Date: 2014-9-26
Title: Android声波通信
Category: Android
Tags: Android, voice
Slug: android_voice_communication
Status: draft


参考：

[Quietnet](https://github.com/Katee/quietnet)


### 发送部分

通过超声波(19.1kHz)携带信息，OOK调制，叠加一段音乐后发送。

#### 编码

由于采用了较简单的OOK调制，所以要在调制前把目标信息编码成二进制。采用[这个Python工程](https://github.com/Katee/quietnet)的编码。

编码采用类似霍夫曼编码的思路，但是为了在接收时判断字符的开始结束，引入了对编码的限制。因为接收时通过两个连续的0判定一个自负的结束，所以要求编码首尾都是1，而且不出现连续的0。

#### 调制

每个bit字符占用3个chunk，即重复3遍发送，这是为了在接收时方便判定同步，否则如果接收的采样区间跨越了0和1两个不同的比特，就会造成解调错误。

采用OOK调制。1bit对应有声波，声波波形采用正弦波，与采样率相关，用如下方法计算数组的值；0bit对应没有声波。

```
for (int j = 0; j < Constants.DATASIZE; j++) {
    tone[j] = Math.sin(2 * Math.PI * freq
        * ((double) (j + offset) / Constants.RATE));
}
```

调制以后如果直接发送已经可以正常接收解调了，不过这样由于声音经常发生从0跳变到很大，手机发送时会出现杂音，所以做了一个平滑处理，这也是参考了[这个Python工程](https://github.com/Katee/quietnet)，使音量平滑上升和下降，有效避免杂音。

####叠加


为了让人耳直观的感受到当前有信息正在发送，所以在超声波之上叠加一段正常频率范围的音乐。经过查阅资料研究，19kHz的超声和正常频率之间不会发生担心的混频现象。

叠加直接将两个声波的short数组按一定权值相加即可。

```java
for (int i = 0; i < background.length; i++) {
    background[i] = (short) (background[i] + 0.8 * data[i % data.length]);
}
```

另外，携带信息的超声波信号可能会比背景声音更长，所以在这种情况下要扩展背景声音的长度。

### 接收部分

#### 解调

用FFT变换做解调。这是为了去除叠加的背景音乐和周围环境噪声的影响，否则在采样率相对于信号频率不太高的情况下，使用简单的过零检测误码率极大。

由AudioRecord接收到的数组按chunk的大小分片，每一片单独处理。利用FFT变换，可以计算出每一片在19kHz频率的功率，如果超过一定阈值，判定当前是1bit，如果没有超过，则当前是0bit。

FFT变换使用`org.apache.commons.math3.transform`库，

```java
transformer = new FastFourierTransformer(DftNormalization.STANDARD);
Complex[] fftResultComplex = transformer.transform(dataComplex, TransformType.FORWARD);
for (int i = 0; i < fftResultComplex.length; i++) {
    ret[i] = (int) Math.round(fftResultComplex[i].abs());
}
```

符号同步问题：当在一直收到0时，认为当前还没有开始发送，一旦出现了一个超过阈值的分片，即开始发送信号，那么这个分片和后面的2个组成一个3个chunk大小的分组，他们代表的是一个bit，那么同步就完成了，再后边的分片就可以直接认为是三个一组进行判定了。

#### 解码


解码器中保存解调器解调得到的bit流，因为采用了特殊的编码方式，接收时如果出现连续的0则认为是一个字符结束，就将之前的bit与码表中做对比，即可判定出发送方的字符。


### 发送和识别有效信息

信息发送是循环的，为了接收方判断接收到的字符串是否是完整的uid串，在发送时将uid首尾用`B`、`E`字符标明，当接收方接收到`B`字符时才开始记录，当接收到`E`时认为接收完毕，这时就可以取出中间的字符串认为是要传递的有效信息。


