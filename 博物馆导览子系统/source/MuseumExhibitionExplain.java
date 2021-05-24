package Servlet;

import System.*;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.apache.catalina.filters.ExpiresFilter;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Map;

@WebServlet("/MuseumExhibitionExplain")
public class MuseumExhibitionExplain extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response){
        JSONObject JR=new JSONObject();
        DB ExhibitionDB = null;
        try {
            String exhname = request.getParameter("exhname");
            ExhibitionDB = new DB("MUSEUM");
            if (ExhibitionDB.Error()) {
                JR.put("STATUS","001");
                JR.put("Error","ExhibitionDB connection Error!");
                throw new Exception(JR.getString("Error"));
            }
            String sql ="select * from MUSEUM.exhibition where exhname='"+exhname+"';";
            ArrayList<Map<String,String>> res1=ExhibitionDB.Select(sql);
            if(res1.size()!=1){
                JR.put("STATUS","002");
                JR.put("Error","The number of Exhibition is not 1!");
                throw new Exception(JR.getString("Error"));
            }
            String ExhibitionID=res1.get(0).get("id");
            sql=new String("select * from MUSEUM.explain where ExhibitionID="+ExhibitionID+" and type =2 and status =1;");
            ArrayList<Map<String,String>> res =ExhibitionDB.Select(sql);
            System.out.println(res.size());
            JSONArray JA=new JSONArray();
            JR.put("resultSize",res.size());
            JR.put("result",res);
            JR.put("STATUS","0");
            JR.put("Error","");


        }catch (Exception e){
            System.out.println(e.getMessage());
        }finally {
            response.setHeader("Content-Type", "text/html;charset=UTF-8");
            response.setCharacterEncoding("UTF-8");
            try (PrintWriter pw = response.getWriter()) {
                pw.write(JSON.toJSONString(JR));
            }catch (Exception e){
                System.out.println("Unknown Error!");
            }
            if(ExhibitionDB!=null){
                ExhibitionDB.Close();
            }
        }
    }
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response){
        JSONObject JR=new JSONObject();
        DB ExhibitionDB = null;
        try {
            String exhname = request.getParameter("exhname");
            ExhibitionDB = new DB("MUSEUM");
            if (ExhibitionDB.Error()) {
                JR.put("STATUS","001");
                JR.put("Error","ExhibitionDB connection Error!");
                throw new Exception(JR.getString("Error"));
            }
            String sql ="select * from MUSEUM.exhibition where exhname='"+exhname+"';";
            ArrayList<Map<String,String>> res1=ExhibitionDB.Select(sql);
            if(res1.size()!=1){
                JR.put("STATUS","002");
                JR.put("Error","The number of Exhibition is not 1!");
                throw new Exception(JR.getString("Error"));
            }
            String ExhibitionID=res1.get(0).get("id");
            sql=new String("select * from MUSEUM.explain where ExhibitionID="+ExhibitionID+" and type =2 and status =1;");
            ArrayList<Map<String,String>> res =ExhibitionDB.Select(sql);
            System.out.println(res.size());
            JSONArray JA=new JSONArray();
            JR.put("resultSize",res.size());
            JR.put("result",res);
            JR.put("STATUS","0");
            JR.put("Error","");


        }catch (Exception e){
            System.out.println(e.getMessage());
        }finally {
            response.setHeader("Content-Type", "text/html;charset=UTF-8");
            response.setCharacterEncoding("UTF-8");
            try (PrintWriter pw = response.getWriter()) {
                pw.write(JSON.toJSONString(JR));
            }catch (Exception e){
                System.out.println("Unknown Error!");
            }
            if(ExhibitionDB!=null){
                ExhibitionDB.Close();
            }
        }
    }
}
