# 1 实验内容：  

设计一个应用软件，以实现将正则表达式-->NFA--->DFA-->DFA最小化-->词法分析程序

# 2 实验要求：  

 （1）要提供一个正则表达式的输入界面，让用户输入正则表达式（可保存、打开保存着正则表达式的文件）  
 
 （2）需要提供窗口以便用户可以查看转换得到的NFA（用状态转换表呈现即可）  
 
 （3）需要提供窗口以便用户可以查看转换得到的DFA（用状态转换表呈现即可）  
 
 （4）需要提供窗口以便用户可以查看转换得到的最小化DFA（用状态转换表呈现即可）  
 
 （5）需要提供窗口以便用户可以查看转换得到的词法分析程序（该分析程序需要用C语言描述）  
 
 （6）应该书写完善的软件文档  
 
# 3 实现  
编译原理的实验作业是比较难的，然后我就想着网上的都是C++实现的，我放一个py实现的，供学弟学妹们参考，避免大家抄重复了哈哈哈（不是）
## 说明  
本程序的操作数只能支持a-z，运算符有+ * | & ( )  
&符号是连接，一般不显示，但是为了处理连接用一个&代替  
  
## 3.1 正则表达式的预处理
我们要将输入的中缀表达式转化为后缀表达式(逆波兰表达式)，这有助于我们处理运算符的优先级。运算符号的优先级为 __)__ > __闭包*__ = __正闭包+__ > __或|__ > __连接&__  > __(__

为了将中缀表达式转化为后缀表达式，我们需要一个栈作为辅助容器。  

算法思想是：  依次扫描输入的正则表达式，  

1)如果遇到操作数，直接输出  

2)如果遇到运算符：  
①遇到(直接进栈  
②遇到)，将栈内的运算符依次输出，直到遇到(为止，但(不输出，)也不进栈  
③遇到*、&、+：  依次将栈内优先级大于等于当前运算符的符号弹出并输出，直到栈顶的运算符的优先级小于当前运算符，然后再将当前运算符入栈  

3)扫描完成后，如果栈不为空，将栈内运算符依次弹出并输出  

然后我们就得到了后缀表达式  
__噢对！不要忘了检查输入的正则表达式的合法性，本程序只做了简单的非法情况测试__

## 3.2 后缀表达式转化为NFA
 NFA的数据结构:  
 
 	class NFAstate:
   	  index = 0
      def __init__(self):
          # 当前节点编号
          self.index = NFAstate.index
          # 当前节点值
          self.value = '#'
          # 当前结点连接到的编号
          self.chTrans = -1
          # 当前节点通过ε转移到的状态号集合
          self.eps = set()
          NFAstate.index += 1
 	ns_list = [NFAstate() for i in range(128)]  
  
  	class NFA:    
      def __init__(self, num):
          if num == -1:
              self.head = -1
              self.tail = -1
          else:
              self.head = ns_list[num]
              self.tail = ns_list[num + 1]  
              
简单思想就是，从头扫描后缀表达式：  
1)遇到操作数，从ns_list里取出一个NFAstate，将操作数的值赋予它，并且这个NFAstate指向下一个NFAstate，然后将取出来的这个NFAstate放入栈中。 __非常需要注意的是：不管是NFA还是DFA，边上的值是操作数或运算符，而不是点的值。这是我当初初学的时候理解错的一个点。所以，两个结点连起来的边才能表示一个操作数或运算符。__  
2)遇到运算符：  
①闭包*:  
新建一个NFAstate，然后再从栈中取出一个NFAstate，具体操作如图  
![闭包](https://github.com/Gao-JF/Regular-Expression-to-DFA/blob/main/%E9%97%AD%E5%8C%85.png?raw=true)   

②正闭包+：  
新建一个NFAstate，然后再从栈中取出一个NFAstate，具体操作如图  
![正闭包](https://github.com/Gao-JF/Regular-Expression-to-DFA/blob/main/%E6%AD%A3%E9%97%AD%E5%8C%85.jpg?raw=true)   

③或|：  
新建一个NFAstate，然后再从栈中取出两个NFAstate，具体操作如图  
![或](https://github.com/Gao-JF/Regular-Expression-to-DFA/blob/main/%E6%88%96.png?raw=true)   

④连接&：  
从栈中取出两个NFAstate，具体操作如图  
![连接](https://github.com/Gao-JF/Regular-Expression-to-DFA/blob/main/%E8%BF%9E%E6%8E%A5.png?raw=true)   


## 3.3 NFA转化为DFA  
基本思路  
1)首先找出初始状态的ε闭包
2)遍历终结符集（也就是操作数），对每一个终结符做move操作  
move操作：就是用闭包的所有状态去匹配当前的标识符，得到新的集合  
3)找不到新的集合，遍历结束  

## 3.4 DFA最小化
用这个图做例子：  
![DFA](https://github.com/Gao-JF/Regular-Expression-to-DFA/blob/main/dfa.png?raw=true)   
1)分组，得到 {A,B,C,D} {E}  
2){E} 独自分组，无法操作。 {A,B,C,D}做a操作，发现都转为状态B，做b操作，A，B，C在 {A,B,C,D} 组内成员，而D在另一个组内，重新分组得到 {A,B,C} {D} {E}  
3){D} {E}无法操作， {A,B,C} 做a操作，都在同一组内，做b操作，B不在同一组内，重新划分，重新分组得到 {A,C} {B} {D} {E}  
4){A,C} 进行a操作和b操作都在同一组内，无法继续向下划分了。操作到此结束。可以将 {A,C}合并  
