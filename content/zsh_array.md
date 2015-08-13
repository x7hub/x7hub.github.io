Date: 2013-11-30
Title: 对比zsh和bash中的数组与关联数组
Category: Linux
Tags: Linux, shell
Slug: zsh_array

参考：

Linux Shell脚本攻略 人民邮电出版社


### 数组

可以这样定义数组，在`bash`和`zsh`都可以，

```sh
array_var=(1 2 3 4 5 6)
```

但是，读数组的时候有区别，在`bash`中，数组索引以`0`开始，符合一般习惯，
```sh
[x7@localhost ~]$ array_var=(1 2 3 4 5 6)
[x7@localhost ~]$ echo ${array_var}
1
[x7@localhost ~]$ echo ${array_var[0]}
1
```

但是，在`zsh`中，数组索引以`1`开始，索引`0`是空的，
```sh
~/workspace/shell % array_var=(1 2 3 4 5 6)
~/workspace/shell % echo ${array_var[0]}

~/workspace/shell % echo ${array_var[1]}
1
~/workspace/shell % echo ${array_var[2]}
2
~/workspace/shell % echo ${array_var[6]}
6
~/workspace/shell % echo ${array_var[7]} 

~/workspace/shell % echo ${array_var}
1 2 3 4 5 6
~/workspace/shell % echo ${array_var[*]} 
1 2 3 4 5 6
~/workspace/shell % echo ${array_var[@]} 
1 2 3 4 5 6
~/workspace/shell % echo ${#array_var[*]}
6
```

### 关联数组

在`bash`中，可以这样声明关联数组，
```sh
[x7@localhost ~]$ declare -A ass_array
[x7@localhost ~]$ ass_array=([index1]='val1' [index2]='val2')
```

但是在`zsh`中就不行，
```sh
~ % declare -A ass_array 
~ % ass_array=([index1]='val1' [index2]='val2')
zsh: no matches found: [index1]=val1
```

只能这样才行，
```sh
~ % declare -A ass_array
~ % ass_array[index1]='val1'
```

另外，在`bash`访问数组需要加大括号，不加的话拿到的是奇怪的东西，
```sh
[x7@localhost ~]$ echo ${ass_array[index1]}
val1
[x7@localhost ~]$ echo $ass_array[index1]
[index1]
```
在`zsh`中就可以不用大括号直接拿，
```sh
~ % echo ${ass_array[index1]}
val1
~ % echo $ass_array[index1]
val1
```

### 暂时就这些

看来zsh和bash有好多不同啊，以前都没在意过。。。


