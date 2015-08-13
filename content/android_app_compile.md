Date: 2013-10-08
Title: Android源码中日历模块单独编译
Category: Android
Tags: Android
Slug: android_app_compile

参考:

[在Eclipse中开发Android系统的内置应用(Mms, Contacts ect)](http://blog.csdn.net/xixinyan/article/details/6942074)

[android4.0.3 联系人Contacts应用导入到eclipse中编译运行之一](http://blog.csdn.net/zhu_apollo/article/details/8760025)



### Android 源码下载：
利用`repo`工具下载Google原生的Android源码。参考[Google官方文档](http://source.android.com/source/downloading.html)。

高通芯片对应的Android[源码下载](https://www.codeaurora.org/xwiki/bin/QRD-Android/)。

### Android源码结构：
Google提供的Android包含了：Android源代码，工具链，基础C库，仿真环境，开发环境等。

第一级别的目录和文件如下所示：
```
　　----------------
　　　|-- Makefile            全局的Makefile
　　　|-- build               系统编译规则和配置所需要的脚本和工具
　　----------------
　　　|-- prebuilt        各种平台编译工具链
　　　|-- bionic              基础C库源代码
　　----------------
　　　|-- frameworks *        Android应用程序的核心框架层(java及C++语言)
　　　|-- system     *        底层文件系统/库/应用及组件(C语言)
　　　|-- dalvik              JAVA虚拟机
　　　|-- external            android使用的一些额外开源库
　　　|-- libcore             与媒体播放框架代码相关
　　----------------
　　　|-- packages            各种应用程序实例
　　　|-- development         程序开发所需要的实例/模板/工具
　　----------------
　　　|-- ndk
　　　|-- sdk
　　　|-- cts                 Android CTS兼容性规范测试用例
　　----------------
　　　|-- vendor     *        厂商定制代码
　　　|-- device     *        厂商定制代码
　　　|-- hardware   *        一些与硬件相关的库，部分厂家开源的硬解适配层HAL代码
　　　|-- kernel     *        Linux源代码
　　　|-- bootable            引导加载器
　　　|-- recovery            与目标的恢复功能相关
　　　----------------
```
`packages`中包含两个主要目录，其中`apps`中是Android中的各种应用程序，`providers`是一些内容提供者（是内部自带的数据库源程序）。两个目录的内容大都是使用JAVA编写的程序，各个文件夹的层次结构是类似的。

作为基于SDK的开发者需要的是`packages/apps`目录下的程序实例。

### Calendar应用在eclipse中单独编译

复制出`packages/apps/Calendar`文件夹，其中包括了Calendar应用的主要代码。但是如果直接import到eclipse中，会因为对源码中的其他文件的依赖而报错不能编译。因此，需要在源码包中找到缺少的依赖文件，并引入到单独复制出的Calendar工程中，将所有因依赖产生的错误解决后，就可以编译运行了。

解决Calendar应用的依赖文件时遇到两种类型：

* 由于java文件缺失造成的依赖错误。在eclipse的代码框中报错，显示找不到类定义。出现这种错误时，应该在Android源码中找到报错的类对应的定义文件，通常为`java`或`aidl`文件，将文件复制到Calendar工程相应的目录下，可以解决报错。例如，`com.android.calendar`包中的`CalendarEventModel.java`文件中，`import com.android.common.Rfc822Validator`语句报错，于是在源码目录中搜索`Rfc822Validator.java`，找到`frameworks/ex/common/java/com/android/common/Rfc822Validator.java`，将`Rfc822Validator.java`复制到`Calendar/src/com/android/common/`文件夹下，在eclipse中刷新整个工程目录，报错的语句就被解决了。

* 由于资源文件造成的依赖错误。为了解决找不到类定义的错误，在Calendar工程中引入了Android源码中其他目录的`java`文件，这些文件会调用到各自目录的`res`文件，都需要将他们引入到Calendar工程中。例如，为了解决`EditEventView.java`的包中的错误，引入了`com.android.ex.chips`包中的`RecipientEditTextView.java`文件，而其中引用的`R.string.copy_number`不存在，就需要在源码中的`com.android.ex.chips`包里找到`strings.xml`中的`copy_number`项，复制到Calendar工程中的`strings.xml`中。

为了在源码环境外编译原生Calendar应用，总共引入了以下源码中的文件。其中，首行表示Calendar工程中报错的文件，为了解决报错引入了随后几行的文件。
```
　　CalendarEventModel.java
　　frameworks/ex/common/java/com/android/common/Rfc822Validator.java
　　　　　
　　DeleteEventHelper.java
　　frameworks/opt/calendar/src/com/android/calendarcommon/EventRecurrence.java

　　EmailAddressAdapter.java
　　frameworks/ex/common/java/com/android/common/contacts/BaseEmailAddressAdapter.java
　　frameworks/ex/common/java/com/android/common/widget/CompositeCursorAdapter.java
　　frameworks/ex/chips/src/com/android/ex/chips/AccountSpecifier.java
　　
　　GoogleCalendarUriIntentFilter.java
　　frameworks/opt/calendar/src/com/android/calendarcommon/DataException.java
　　frameworks/opt/calendar/src/com/android/calendarcommon/Duration.java

　　RecipientAdapter.java
　　frameworks/ex/chips/src/com/android/ex/chips/BaseRecipientAdapter.java
　　frameworks/ex/chips/src/com/android/ex/chips/Queries.java
　　frameworks/ex/chips/src/com/android/ex/chips/RecipientEntry.java
　　frameworks/ex/chips/res/layout/chips_recipient_dropdown_item.xml
　　frameworks/ex/chips/res/drawable/list_item_font_primary.xml
　　frameworks/ex/chips/res/drawable/list_item_font_secondary.xml

　　EditEventHelper.java
　　frameworks/opt/calendar/src/com/android/calendarcommon/RecurrenceProcessor.java
　　frameworks/opt/calendar/src/com/android/calendarcommon/RecurrenceSet.java
　　frameworks/opt/calendar/src/com/android/calendarcommon/ICalendar.java

　　EditEventView.java
　　frameworks/ex/common/java/com/android/common/Rfc822InputFilter.java
　　frameworks/ex/chips/src/com/android/ex/chips/ChipsUtil.java
　　frameworks/ex/chips/src/com/android/ex/chips/RecipientEditTextView.java
　　frameworks/ex/chips/src/com/android/ex/chips/RecipientAlternatesAdapter.java
　　frameworks/ex/chips/src/com/android/ex/chips/RecipientChip.java
　　frameworks/ex/chips/res/values/strings.xml
　　frameworks/ex/chips/res/values/attrs.xml
　　frameworks/ex/chips/res/drawable-{hdpi,mdpi,xhdpi}/{chip_background.9.png,chip_delete.png,chip_background_invalid.9.png,chip_background_selected.9.png}
　　frameworks/ex/chips/src/com/android/ex/chips/SingleRecipientArrayAdapter.java
```
