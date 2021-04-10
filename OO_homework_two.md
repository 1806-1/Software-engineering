# **第二章 类与对象**
# 2.1
(1) 友元函数  
(2) 所在对象的起始地址  
(3) 对象  
(4) `friend void fun()`  
(5) 所在对象的起始地址


# 2.2

(1) B  
(2) C  
(3) D  
(4) A  
(5) A  
(6) C  
(7) A  
(8) A

# 2.3

(1) 
把数据结构和对数据结构进行操作的方法封装形成一个个的对象。  
(2) 
类是一种由用户定义的复杂数据类型，它是将不同类型的数据和这些数据的相关操作封装在一起的集合体。  
(3)  
类的实例化结果就是对象，而对一类对象的抽象就是类。  
类就像饼干模子，对象就像饼干。  
(4)  
对象都具有的特征是：静态特征和动态特征。
静态特征是指能描述对象的一些属性，动态特征是指对象表现出来的行为。
例如：一个三角形对象，它的边长就是属性。  
(5)  
public, private, protect。  
(6)  
这种函数会自动为内联函数，这种函数在函数调用的地方在编译阶段都会进行代码替换。  
当函数声明在类内，但定义在类外的看是否有inline修饰符，如果有就是内联函数，否则不是。  
(7)  
默认构造函数，拷贝构造函数，析构函数，赋值函数。  
(8)  
a.当类的一个对象去初始化该类的另一个对象时；  
b.如果函数的形参是类的对象，调用函数进行形参和实参结合时；  
c.如果函数的返回值是类对象，函数调用完成返回时。  
(9)  
a.先调用基类构造函数;  
b.按声明顺序初始化数据成员;  
c.最后调用自己的构造函数。  
(10)  
常对象是指在任何场合都不能对其成员的值进行修改的对象。  
(11)  
友元函数，继承，公有成员函数。  
(12)  
对象生命周期结束时。  
(13)  
它的次序完全不受它们在初始化表中次序的影响，只有成员对象在类中声明的次序来决定的。  
(14)  
构造函数可以被重载，析构函数不可以被重载。因为构造函数可以有多个且可以带参数，而析构函数只能有一个，且不能带参数。  
(15)  
只可以由本类中的成员函数和友元函数访问。

# 2.4  
(1)  
```cpp
#include<iostream>

using namespace std;

class Samp
{
public:
	void Setij(int a, int b) { i = a, j = b; }
	~Samp() 
	{
		cout << "Destroying.." << i << endl;
	}
	int GetMuti() { return i * j; }
protected:
	int i;
	int j;
};

int main() {
	Samp* p;
	p = new Samp[5];
	if (!p) {
		cout << "Allocation error\n";
		return 1;
	}
	for (int j = 0; j < 5; j++)
		p[j].Setij(j, j);
	for (int k = 0; k < 5; k++)
		cout << "Muti[" << k << "] is:" << p[k].GetMuti() << endl;
//                                         --------------
	Samp();
//  -------
	return 0;
}

```
(2)

```cpp
#include<iostream>
#include<math.h>

using namespace std;

void area() 
{
	double a, b, c;
	cout << "Input a b c:";

	cin >> a >> b >> c;
//  -------------------
		if (a + b > c && a + c > b && c + b > a)
		{
			double l = (a + b + c) / 2;
			double s = sqrt(l * (l - a) * (l - b) * (l - c)); // 海伦公式
//          -------------------------------------------------
				cout << "The area is:" << s << endl;
		}
		else {
			cout << "Error" << endl;
		}
}
void main() 
{
	area();
}

```

# 2.5
(1)
```cpp
//程序实现两个字符串相加
#include<iostream>
#include<string>

using namespace std;

class String
{
	
public:
	String()
	{
		static int i = 1;
		cout << "String" << i++ << " have been created " << endl;
	}

	~String()
	{
		cout << read << " have been destroied" << endl;
	}

	String& operator += (const String& t)
	{
		if (this != &t)
		{
			read += t.read;
		}

		return *this;
	}
	String& operator = (const String& t)
	{
		if (this != &t)
		{
			read = t.read;
		}

		return *this;
	}

	void get()
	{
		cout << "plaese input string 'read':";
		cin >> read;
		cout << endl;
	}

	void out()
	{
		cout << read ;
	}

private:
	string read;

};

int main()
{
	String test1;
	String test2;
	String test3;

	test1.get();
	test2.get();
	test3 = test1;
	test1 += test2;
	

	test1.out();
	cout << " = ";
	test3.out();
	cout << " + ";
	test2.out();

	cout << endl << endl;

}
```
(2)
```cpp
//程序从student.txt文件中读取学生信息，求总成绩排序后输出到sotr_s.txt文件中
//文件中学生信息格式为
//name_ gender_ ID_ selfgrade[0] ... selfgrade[7]
//输出文件学生信息格式为
//name_ gender_ ID_ selfgrade[0] ... selfgrade[7] sum_
#include<iostream>
#include<string>
#include<algorithm>
#include<fstream>

using namespace std;
bool flag = 0;


class Student
{
	
public:
	string name_;
	bool gender_ = 1; // 1 is for male
	string ID_;
	int selfgrade_[8];
	int sum_ ;

	Student()
	{

	}
	void sum()
	{
		int sum = 0; 
		for (int i = 0; i < 8; i++)
		{
			sum += selfgrade_[i];
		}
		sum_ = sum;
	}
	
private:
	
};

bool cmp(Student a, Student b)
{
	return (a.sum_ > b.sum_);
}

int main()
{
	Student s[1000];
	int j = 0;
	ifstream input;

	input.open("student.txt");
	int tail = 0;
	int i = 0;
	while (!input.eof())
	{
		input >> s[i].name_ >> s[i].gender_ >> s[i].ID_;
		for (int j = 0; j < 8; j++)
			input >> s[i].selfgrade_[j];
		i++;
	}
	int number = i;
	for (int i = 0; i < number; i++)
	{
		s[i].sum();
	}

	sort(s, s + number, cmp);

	ofstream output;
	output.open("sort_s.txt");

	for (int i = 0; i < number; i++)
	{
		output << s[i].name_ << ' ' << s[i].gender_ << ' ' << s[i].ID_ << ' ';
		for (int j = 0; j < 8; j++)
			output << s[i].selfgrade_[j] << ' ';
		output << s[i].sum_ << endl;
	}
}
```



