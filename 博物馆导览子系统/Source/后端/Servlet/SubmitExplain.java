package Servlet;

import System.*;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import jakarta.servlet.*;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import org.apache.tomcat.util.http.fileupload.FileItemFactory;
import org.apache.tomcat.util.http.fileupload.RequestContext;
import org.apache.tomcat.util.http.fileupload.servlet.ServletFileUpload;
import org.apache.tomcat.util.http.fileupload.FileItem;
import org.apache.tomcat.util.http.fileupload.disk.DiskFileItemFactory;

import javax.swing.plaf.synth.SynthTabbedPaneUI;
import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@WebServlet("/SubmitExplain")
public class SubmitExplain extends HttpServlet {
    public void doPost(HttpServletRequest request, HttpServletResponse response) {
        DB ExplainDB = null;
        JSONObject JR = new JSONObject();
        String Jsonstring;
        String type = null;
        String museumID = null;
        String exhibitionID = null;
        String collectionID = null;
        String explainName = null;
        String userID = null;
        String intro = null;
        String audio = null;
        try {
            ExplainDB = new DB("MUSEUM");
            if (ExplainDB.Error()) {
                JR.put("success", "false");
                JR.put("Error", "ExhibitionDB connection Error!");
                throw new Exception(JR.getString("Error"));
            }

            Jsonstring = request.getParameter("JSONString");
            JSONObject obj = JSON.parseObject(Jsonstring);

            type = obj.getString("type");
            museumID = obj.getString("museumID");
            exhibitionID = obj.getString("exhibitionID");
            collectionID = obj.getString("collectionID");
            explainName = obj.getString("explainName");
            userID = obj.getString("userID");
            userID="1";
            intro = obj.getString("intro");
            audio = obj.getString("audio");
        } catch (Exception e) {
        }

        try{
            FileItemFactory factory =new DiskFileItemFactory();
            ServletFileUpload upload = new ServletFileUpload(factory);
            List<FileItem> items = upload.parseRequest((RequestContext) request);
            String filename = "";
            InputStream is = null;
            for (FileItem item : items) {
                if (item.isFormField()) {
                    if (item.getFieldName().equals("filename")) {
                        if (!item.getString().equals(""))
                            filename = item.getString("UTF-8");
                    }
                }
                else if (item.getName() != null && !item.getName().equals("")) {
                    filename = item.getName().substring(item.getName().lastIndexOf("\\") + 1);
                    is = item.getInputStream();
                }
            }
//            filename = filename.substring(2);
            audio = filename;
            // 将路径和上传文件名组合成完整的服务端路径
            String upLoadPath = "F:\\data\\audio\\";
            filename = upLoadPath + filename;
            if (new File(filename).exists()) {
                new File(filename).delete();
            }
            if (!filename.equals("")) {
                FileOutputStream fos = new FileOutputStream(filename);
                byte[] buffer = new byte[8192];
                int count = 0;
                while ((count = is.read(buffer)) > 0) {
                    fos.write(buffer, 0, count);
                }
                fos.close();
                is.close();
                SFTPConnection sftp = new SFTPConnection("root", "CS2018se.", "182.92.221.222", 22);
                sftp.uploadFile("/var/www/html/data/audio/", filename);
            }
        }
        catch (Exception e) {
            if(e.getMessage().equals("fail sql")){
                System.out.println("fail sql");
            }
        }


        try {
            String sql=null;
            if(type.equals("")) {
                JR.put("success", "false");
                throw new Exception("false type");
            }else if(type.equals("1")){
                sql = new String("INSERT INTO `MUSEUM`.`explain` (`type`, `museumID`, `exhibitionID`, `collectionID`, `name`, `userID`, `introduction`, `audio`, `status`) " +
                        "VALUES ('" + type + "', '" + museumID + "', '" + exhibitionID + "', '" + collectionID + "', '" + explainName + "', '" + userID + "', '" + intro + "', 'http://182.92.221.222/data/audio/" + audio + "', '0');");
            }else if(type.equals("2")){
                ArrayList<Map<String,String>> res=ExplainDB.Select("SELECT * FROM MUSEUM.exhibition where id = "+exhibitionID+";");
                if(res.size()!=1){
                    JR.put("success", "false");
                    JR.put("Error","The number of Exhibition is not 1!");
                    throw new Exception(JR.getString("Error"));
                }
                String museumName=res.get(0).get("museumName");
                res=ExplainDB.Select("SELECT * FROM MUSEUM.overview where bwgname='"+museumName+"';");
                if(res.size()!=1){
                    JR.put("success", "false");
                    JR.put("Error","The number of museum is not 1!");
                    throw new Exception(JR.getString("Error"));
                }
                museumID=res.get(0).get("id");
                sql = new String("INSERT INTO `MUSEUM`.`explain` (`type`, `museumID`, `exhibitionID`, `collectionID`, `name`, `userID`, `introduction`, `audio`, `status`) " +
                        "VALUES ('" + type + "', '" + museumID + "', '" + exhibitionID + "', '" + collectionID + "', '" + explainName + "', '" + userID + "', '" + intro + "', 'http://182.92.221.222/data/audio/" + audio + "', '0');");
            }else if(type.equals("3")){
                ArrayList<Map<String,String>> res=ExplainDB.Select("SELECT * FROM MUSEUM.collection where id = "+collectionID+";");
                if(res.size()!=1){
                    JR.put("success", "false");
                    JR.put("Error","The number of Exhibition is not 1!");
                    throw new Exception(JR.getString("Error"));
                }
                String museumName=res.get(0).get("museumName");
                res=ExplainDB.Select("SELECT * FROM MUSEUM.overview where bwgname='"+museumName+"';");
                if(res.size()!=1){
                    JR.put("success", "false");
                    JR.put("Error","The number of museum is not 1!");
                    throw new Exception(JR.getString("Error"));
                }
                museumID=res.get(0).get("id");
                sql = new String("INSERT INTO `explain` (`type`, `museumID`, `exhibitionID`, `collectionID`, `name`, `userID`, `introduction`, `audio`, `status`) " +
                        "VALUES ('" + type + "', '" + museumID + "', '" + exhibitionID + "', '" + collectionID + "', '" + explainName + "', '" + userID + "', '" + intro + "', 'http://182.92.221.222/data/audio/" + audio + "', '0');");

            }

            if (!ExplainDB.Update(sql)) {
                JR.put("success","false");
                throw new Exception("fail sql");
            }else {
                JR.put("success","true");
            }
        } catch (Exception e) {
            System.out.println("fail sql");
        }finally {
            response.setHeader("Content-Type", "text/html;charset=UTF-8");
            response.setCharacterEncoding("UTF-8");
            try (PrintWriter pw = response.getWriter()) {
                pw.write(JSON.toJSONString(JR));
            }catch (Exception e){
                System.out.println("Unknown Error!");
            }
            if(ExplainDB!=null){
                ExplainDB.Close();
            }
        }
    }

//        try {
//            request.setCharacterEncoding("UTF-8");
//            // 下面的代码开始使用Commons-UploadFile组件处理上传的文件数据
//            FileItemFactory factory = new DiskFileItemFactory(); // 建立FileItemFactory对象
//            ServletFileUpload upload = new ServletFileUpload(factory);
//            // 分析请求，并得到上传文件的FileItem对象
//            List<FileItem> items = upload.parseRequest((RequestContext) request);
//            String filename = ""; // 上传文件保存到服务器的文件名
//            InputStream is = null; // 当前上传文件的InputStream对象
//            // 循环处理上传文件
//            for (FileItem item : items) {
//                // 处理普通的表单域
//                if (item.isFormField()) {
//                    if (item.getFieldName().equals("filename")) {
//                        // 如果新文件不为空，将其保存在filename中
//                        if (!item.getString().equals(""))
//                            filename = item.getString("UTF-8");
//                    }
//                }
//                // 处理上传文件
//                else if (item.getName() != null && !item.getName().equals("")) {
//                    // 从客户端发送过来的上传文件路径中截取文件名
//                    filename = item.getName().substring(item.getName().lastIndexOf("\\") + 1);
//                    is = item.getInputStream(); // 得到上传文件的InputStream对象
//                }
//            }
//            //对filename进行提取
//            filename = filename.substring(2);
////            String filename2=new String(filename);
//            try{
//                String sql=new String("INSERT INTO `MUSEUM`.`explain` (`type`, `museumID`, `exhibitionID`, `collectionID`, `name`, `userID`, `introduction`, `audio`, `status`) "+
//                        "VALUES ('"+type+"', '"+museumID+"', '"+exhibitionID+"', '"+collectionID+"', '"+explainName+"', '"+userID+"', '"+intro+"', 'http://182.92.221.222/data/audio/"+filename+"', '0');");
//                if(!ExplainDB.Update(sql)){
//                    throw new Exception("fail sql");
//                }
//            }catch (Exception e){
//                if(e.getMessage().equals("fail sql")){
//                    throw e;
//                }
//            }
//
//            // 将路径和上传文件名组合成完整的服务端路径
//            String upLoadPath = "F:\\data\\audio\\";
//            filename = upLoadPath + filename;
//            if (new File(filename).exists()) {
//                new File(filename).delete();
//            }
//            if (!filename.equals("")) {
//                FileOutputStream fos = new FileOutputStream(filename);
//                byte[] buffer = new byte[8192];
//                int count = 0;
//                while ((count = is.read(buffer)) > 0) {
//                    fos.write(buffer, 0, count);
//                }
//                fos.close();
//                is.close();
//                SFTPConnection sftp = new SFTPConnection("root", "CS2018se.", "182.92.221.222", 22);
//                sftp.uploadFile("/var/www/html/data/audio/", filename);
//            }
//        }
//        catch (Exception e) {
//            if(e.getMessage().equals("fail sql")){
//                System.out.println("fail sql");
//            }
//        }


}