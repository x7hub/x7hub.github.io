Date: 2014-4-17
Title: 屡败屡战
Category: else
Tags: else
Slug: interview_for_job
Status: draft


###阿里移动客户端 Apr16

* ArrayList和HashMap的下层实现

>ArrayList是数组，HashMap是数组和链表

>[深入Java集合学习系列：ArrayList的实现原理](http://zhangshixi.iteye.com/blog/674856)

>[深入Java集合学习系列：HashMap的实现原理](http://zhangshixi.iteye.com/blog/672697)

* 常用的排序算法有哪些

>[排序算法](http://zh.wikipedia.org/wiki/%E6%8E%92%E5%BA%8F%E7%AE%97%E6%B3%95)

* 快速排序的过程，复杂度是多少，怎么算的

>[快速排序](http://zh.wikipedia.org/wiki/%E5%BF%AB%E9%80%9F%E6%8E%92%E5%BA%8F)

>[快速排序复杂度分析](http://book.51cto.com/art/201108/287089.htm)

* Service在主线程还是子线程

>主

* 为什么需要Service而不用Thread代替

>Activity销毁后不能再持有Thread的引用；不能在不同Activity中控制一个Thread；Thread容易被系统回收

>[Android 中的 Service 全面总结](http://www.cnblogs.com/newcj/archive/2011/05/30/2061370.html)

* Activity退出后它启动的Thread会怎样

>Thread并不会自动随Activity的destroy而关闭，所以必须手动去关闭自己开的线程或者通过boolean的方式让自己开的线程结束运行

>[销毁activity时注意关闭线程](http://www.eoeandroid.com/thread-175819-1-1.html)

* Android系统回收资源的顺序

>按照优先级

>[Android的进程优先级与进程回收](http://www.eoeandroid.com/thread-203499-1-1.html)

* Activity的launchmode属性

>[基础总结篇之二：Activity的四种launchMode](http://blog.csdn.net/liuhe688/article/details/6754323)

* 设置了singleTop属性后，在栈顶的Activity再次被调起，怎么拿到调用的参数？

>onNewIntent

>[Activity的启动模式以及onNewIntent(Intent intent)](http://www.cnblogs.com/shitianzeng/articles/2807062.html)

* 常用的设计模式，画出工厂方法模式的UML，观察者模式中被观察者中存放的是观察者的基类还是子类

>[设计模式 (计算机)](http://zh.wikipedia.org/wiki/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F_(%E8%AE%A1%E7%AE%97%E6%9C%BA))




