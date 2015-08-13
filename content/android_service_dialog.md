Date: 2013-11-05
Title: 对Service中弹出的Dialog设置主题
Category: Android
Tags: Android
Slug: android_service_dialog


参考：

[service中显示一个dialog](http://blog.csdn.net/huxueyan521/article/details/8954844)

[android UI进阶之style和theme的使用](http://www.cnblogs.com/noTice520/archive/2011/02/01/1948738.html)


###简介

有一个Dialog需要在多个应用中的多个位置调用，需要用Intent调起，于是想出的办法是Intent调起一个Service，重写这个Service的`onStartCommand`方法在其中弹出Dialog。弹出Dialog后发现主题与软件整体采用的`Theme.Holo.Light`不一致，于是找到了为弹出的对话框设置主题的方法，在文中给出。

###Services中弹出Dialog

新建一个Service并在`AndroidManifest.xml`中声明`Service`和`intent-filter`，在需要的地方用Intent调起，不谈。

用`startService(intent)`调起Service后的操作需要重写`onStartCommand`方法，在其中尝试按照平常的方法调起Dialog：
```java
Dialog dialog = new Dialog(context);
dialog.setContentView(R.layout.something);
dialog.show();
```

这样尝试调起Dialog会引起错误：
```
11-05 22:13:04.439: E/AndroidRuntime(18271): FATAL EXCEPTION: main
11-05 22:13:04.439: E/AndroidRuntime(18271): java.lang.RuntimeException: Unable to start service edu.bupt.contacts.edial.EdialService@428be268 with Intent { act=edu.bupt.action.EDIAL (has extras) }: android.view.WindowManager$BadTokenException: Unable to add window -- token null is not for an application
11-05 22:13:04.439: E/AndroidRuntime(18271): 	at android.app.ActivityThread.handleServiceArgs(ActivityThread.java:2515)
11-05 22:13:04.439: E/AndroidRuntime(18271): 	at android.app.ActivityThread.access$1900(ActivityThread.java:133)
11-05 22:13:04.439: E/AndroidRuntime(18271): 	at android.app.ActivityThread$H.handleMessage(ActivityThread.java:1300)
11-05 22:13:04.439: E/AndroidRuntime(18271): 	at android.os.Handler.dispatchMessage(Handler.java:99)
11-05 22:13:04.439: E/AndroidRuntime(18271): 	at android.os.Looper.loop(Looper.java:137)
11-05 22:13:04.439: E/AndroidRuntime(18271): 	at android.app.ActivityThread.main(ActivityThread.java:4794)
11-05 22:13:04.439: E/AndroidRuntime(18271): 	at java.lang.reflect.Method.invokeNative(Native Method)
11-05 22:13:04.439: E/AndroidRuntime(18271): 	at java.lang.reflect.Method.invoke(Method.java:511)
11-05 22:13:04.439: E/AndroidRuntime(18271): 	at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:789)
11-05 22:13:04.439: E/AndroidRuntime(18271): 	at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:556)
11-05 22:13:04.439: E/AndroidRuntime(18271): 	at dalvik.system.NativeStart.main(Native Method)
11-05 22:13:04.439: E/AndroidRuntime(18271): Caused by: android.view.WindowManager$BadTokenException: Unable to add window -- token null is not for an application
11-05 22:13:04.439: E/AndroidRuntime(18271): 	at android.view.ViewRootImpl.setView(ViewRootImpl.java:589)
11-05 22:13:04.439: E/AndroidRuntime(18271): 	at android.view.WindowManagerImpl.addView(WindowManagerImpl.java:326)
11-05 22:13:04.439: E/AndroidRuntime(18271): 	at android.view.WindowManagerImpl.addView(WindowManagerImpl.java:224)
11-05 22:13:04.439: E/AndroidRuntime(18271): 	at android.view.WindowManagerImpl$CompatModeWrapper.addView(WindowManagerImpl.java:149)
11-05 22:13:04.439: E/AndroidRuntime(18271): 	at android.app.Dialog.show(Dialog.java:277)
11-05 22:13:04.439: E/AndroidRuntime(18271): 	at edu.bupt.contacts.edial.EdialService.onStartCommand(EdialService.java:57)
11-05 22:13:04.439: E/AndroidRuntime(18271): 	at android.app.ActivityThread.handleServiceArgs(ActivityThread.java:2498)
11-05 22:13:04.439: E/AndroidRuntime(18271): 	... 10 more
```

这是因为我们的Dialog没有依附于一个Activity，所以需要将其设置成系统界别的Dialog，即全局性质的Dialog，在任何界面下都可以弹出来。
```java
dialog.getWindow().setType(WindowManager.LayoutParams.TYPE_SYSTEM_ALERT);
```

这样就可以成功弹出Dialog了

###为Dialog设置主题

通过上面的方法启动的Dialog，主题默认是`Theme.Holo`，与我们需求的`Theme.Holo.Light`不一致。而且这个Dialog不依附于Activity，无法通过在`AndroidManifest.xml`中为Acitivity设置主题来控制Dialog的主题，于是需要在代码中控制主题。

首先在`values/styles.xml`中设置一个自定义的主题，为了方便做一些修改。也可以直接在下一步使用系统主题。
```xml
<style name="HoloDialogTheme" parent="@android:style/Theme.Holo.Light.Dialog"></style>
```

Dialog类并没有提供直接设置主题的方法，只有一个构造函数（两个参数的构造函数，第二个int参数表示主题）可以设置主题，所以需要重写Dialog类，重写构造函数。
```java

public class HoloDialog extends Dialog {

    public HoloDialog(final Context context, String digits) {
        // super(context);
        super(context, R.style.HoloDialogTheme);
    }
}
```

在Service中启动Dialog时使用这个新建的`HoloDialog`，就可以使用这个主题了。

有了这个类，就可以将之前设置的`TYPE_SYSTEM_ALERT`也放到这里的构造函数中。
```java
public class HoloDialog extends Dialog {

    public HoloDialog(final Context context) {
        // super(context);
        super(context, R.style.HoloDialogTheme);
        this.getWindow().setType(WindowManager.LayoutParams.TYPE_SYSTEM_ALERT);
    }
}
```


