Date: 2015-8-17
Title: MonkeyRunner利用剪贴板输入中文
Category: Android
Tags: Android MonkeyRunner
Slug: monkeyrunner_input_unicode

参考：

[MonkeyRunner](http://developer.android.com/tools/help/MonkeyRunner.html)

[Set clipboard text via adb shell as of API level 11](http://stackoverflow.com/questions/14243427/set-clipboard-text-via-adb-shell-as-of-api-level-11)

### Monkeyrunner不支持中文直接输入

[MonkeyRunner](http://developer.android.com/tools/help/MonkeyRunner.html)是一组[Jython](http://www.jython.org/docs/tutorial/indexprogress.html)环境的Android自动测试工具，通过USB控制Android设备完成点击、拖拽、输入等操作。

`MonkeyDevice`类的`type(String message)`方法支持向设备输入字符串，但是由于Jython本身的原因，无法支持直接输入unicode字符，

```python
device = MonkeyRunner.waitForConnection()
device.type('test') # 成功
device.type('测试') # 无输入
device.type(u'测试') # 无输入
```

解决的思路有两个，

1. 利用Android设备上的输入法输入中文，相对复杂。
2. 利用剪贴板复制粘贴。

下文实现的是利用剪贴板的思路。


### 利用剪贴板输入中文

由PC机通过adb发送中文到Android设备，在设备上接收并将文字放入剪贴板，再通过monkeyrunner控制粘贴到文本框。

#### 由adb传入中文字符

`am startservice`命令可以启指定的Service并传入Extra参数，

```shell
adb shell am startservice -e "text" $message info.x7res.clip/.ClipService
```

`info.x7res.clip`是应用包名，`ClipService`是接收文字的Service，`text`是传入的StringExtra的键。

此处可以直接传入中文，不过为了考虑对Windows的字符编码的兼容性问题，这里传入的是经过`unicode-escape`编码后的ascii字符，在下一步设备上接收时再还原成中文。

#### Android应用接收并放入剪贴板

用Service在后台接收`am startservice`命令传入的Extra参数，需要实现`onStartCommand`方法，

```java
@Override
public int onStartCommand(Intent intent, int flags, int startId) {
    super.onStartCommand(intent, flags, startId);
    String text = intent.getStringExtra("text");
    Log.i(TAG, "text: " + text);
    String textConverted = this.unicodeEscape(text);
    Log.i(TAG, "textConverted: " + textConverted);
    this.setClip(textConverted);
    stopSelf();
    return START_NOT_STICKY;
}
```
unicode-escape的解码可以用`org.apache.commons.lang`库中的`StringEscapeUtils.unescapeJava(input)`方法。

复制到剪贴板，

```java
private void setClip(String text) {
    ClipboardManager clipboard = (ClipboardManager)getSystemService(Context.CLIPBOARD_SERVICE);
    ClipData clip = ClipData.newPlainText("simple text", text);
    clipboard.setPrimaryClip(clip);
}
```

#### monkeyrunner手势控制粘贴

在文本框上长按，出现粘贴按钮，点击按钮粘贴。

```python
view_point = HierarchyViewer.getAbsolutePositionOfView(view)
offset_x = 50
offset_y = 50
self.device.drag((view_point.x + offset_x, view_point.y + offset_y),
                (view_point.x + offset_x, view_point.y + offset_y), 3, 1)
offset_x = 50
offset_y = -20
self.device.touch(view_point.x + offset_x, view_point.y + offset_y, MonkeyDevice.DOWN_AND_UP)
print '\033[1;32m-> \033[0m' + str(view) + " text pasted"
```

长按是利用原地的`drag`实现的。如果利用`press`的`DOWN`和`UP`方法不能实现长按效果。

其中的offset值都是经验值，文本框的编辑位置一般位于`getAbsolutePositionOfView`右下，而长按出现的粘贴按钮一般位于右上。





