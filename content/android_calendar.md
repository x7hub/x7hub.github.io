Date: 2013-10-09
Title: Android原生日历应用分析和简单扩展
Category: android
Tags: android
Slug: android_calendar

参考:

[Android 4.0日历（calendar）源码分析之概览](http://www.jcodecraeer.com/a/anzhuokaifa/androidkaifa/2013/0222/896.html)

[Google Code - android-project-sse-ustc](https://code.google.com/p/android-project-sse-ustc/)

### 简介:

学校实验室的项目，其中一部分需求要修改原生的Android日历应用，加入部分额外的功能。本文介绍对Android源码中日历模块的分析，另外简单实现了农历的显示。[部分修改的源码](https://github.com/x7hub/Calendar_lunar)上传到了github，由于参加与公司的合作项目，所以只提交了完成农历显示的版本，之后的版本不便给出。

本文日历模块特指Android 4.1源码中的`com.android.calendar`，没有对calendar provider做分析。

### 主要结构

首先需要说明，在Google给出的Android代码中单独取出Calendar模块，是不能在eclipse中直接编译运行的。单独编译运行的方法参考[另一篇博文](http://x7hub.github.io/pages/android_app_compile.html)。

* 日历应用有四个主要视图，分别是月视图，周视图，日视图，日程视图。

    ![月视图](http://x7hub.github.io/images/small-android_calendar-02.png)
    ![周视图](http://x7hub.github.io/images/small-android_calendar-03.png)
    ![日视图](http://x7hub.github.io/images/small-android_calendar-04.png)
    ![日程视图](http://x7hub.github.io/images/small-android_calendar-05.png)

    四个视图对应4个Fragment，都附着于`AllInOneActivity`。

    月视图：`month/MonthByWeekFragment.java`

    日视图和周视图：`DayFragment.java`

    日程视图：`agenda/AgendaFragment.java`

* 其他重要视图对应的代码文件：

    日程新建、编辑：`event/EditEventFragment.java`

    日程详细信息：`EventInfoActivity.java`

    设置：`CalendarSettingActivity.java`

    ![日程新建、编辑](http://x7hub.github.io/images/small-android_calendar-06.png)
    ![日程详细信息](http://x7hub.github.io/images/small-android_calendar-07.png) 
    ![设置](http://x7hub.github.io/images/small-android_calendar-08.png)

### 加入农历显示功能

在google-code上找到了一段计算农历的代码，引用的位置[在这里](https://code.google.com/p/android-project-sse-ustc/)。

农历的计算使用代码中的[Lunar.java](https://github.com/x7hub/Calendar_lunar/blob/master/src/edu/bupt/calendar/lunar/Lunar.java)文件。简单看了一下，并没有真的使用复杂的农历算法，而是利用一个数组预存了每一年的初一与1900年1月1日的差数，利用这个数组再做计算。具体参看代码不谈。
```java
    private static int[] lunarInfo = { 19416, 19168, 42352, 21717, 53856, 55632, 91476, 22176, 39632, 21970, 19168, 42422, 42192, 53840, 119381, 46400, 54944, 44450, 38320, 84343, 18800, 42160, 46261, 27216, 27968, 109396, 11104, 38256, 21234, 18800, 25958, 54432, 59984, 28309, 23248, 11104, 100067, 37600, 116951, 51536, 54432, 120998, 46416, 22176, 107956, 9680, 37584, 53938, 43344, 46423, 27808, 46416, 86869, 19872, 42448, 83315, 21200, 43432, 59728, 27296, 44710, 43856, 19296, 43748, 42352, 21088, 62051, 55632, 23383, 22176, 38608, 19925, 19152, 42192, 54484, 53840, 54616, 46400, 46496, 103846, 38320, 18864, 43380, 42160, 45690, 27216, 27968, 44870, 43872, 38256, 19189, 18800, 25776, 29859, 59984, 27480, 21952, 43872, 38613, 37600, 51552, 55636, 54432, 55888, 30034, 22176, 43959, 9680, 37584, 51893, 43344, 46240, 47780, 44368, 21977, 19360, 42416, 86390, 21168, 43312, 31060, 27296, 44368, 23378, 19296, 42726, 42208, 53856, 60005, 54576, 23200, 30371, 38608, 19415, 19152, 42192, 118966, 53840, 54560, 56645, 46496, 22224, 21938, 18864, 42359, 42160, 43600, 111189, 27936, 44448 };
```
在原本的代码中加入两个静态方法，方便在日历需要显示农历的地方调用。
```java
    public static void setLunar(Context context, int year, int month, int day) {

        SharedPreferences prefs = GeneralPreferences
                .getSharedPreferences(context);
        setShowLunch(prefs.getBoolean(GeneralPreferences.KEY_SHOW_LUNAR, false));

        // if (!isSetShowLunar) {
        // return;
        // }
        syear = year;
        smonth = month;
        sday = day;

        Date sDObj = new Date(syear - 1900, smonth - 1, sday);
        Lunar1(sDObj);
    }

    public static String getLunar() {
        if (!isSetShowLunar) {
            return "";
        }
        int sy = (year - 4) % 12;
        String s = "农历 【" + Animals[sy] + "】" + cYear(getYear()) + "年" + " ";

        s = s + ((getIsLeap()) ? "闰" : "") + monthNong[getMonth()] + "月"
                + ((!getIsBig()) ? "小" : "大");

        s = s + cDay(getDay()) + " ";

        s = s + cyclical(getYearCyl()) + "年" + cyclical(getMonCyl()) + "月"
                + cyclical(getDayCyl()) + "日";

        return s;
    }
```

在需要显示农历时，通过`Lunar.java`计算农历。比如`month/SimpleWeekView.java`的`setWeekParams`方法遍历`mNumCells`的过程中加入，
```java

        Context context = getContext();
        Lunar.setLunar(context, time.year, time.month + 1, time.monthDay);
        mLunarNumbers[i] = Lunar.getLunarDayForDisplay();
```

然后在`month/MonthWeekEventsView.java`中`drawWeekNums`方法中遍历`numCount`时加入，
```java

        canvas.drawText(mLunarNumbers[i], x, y + 25, mMonthNumPaint);
```

类似地，可以在`CalendarViewAdapter.java`和`agenda/AgendaByDayAdapter.java`中加入农历显示。


### 加入VCalendar文件分享功能

在`EventInfoFragment.java`中，添加了分享日程的功能，打包成VCalendar类型的vcs文件，通过`Intent.ACTION_SEND`发送到彩信或者邮件应用。

Android源码中包括了一个`ICalendar`类，用于处理VCalendar文件，但是并没有实现(或者是没有保留？)导入导出的功能。`ICanlendar`类内部实现就是对字符串的处理，使用也很简单，导出功能可以用以下代码实现，

```java

    ICalendar.Component component = new ICalendar.Component(
            ICalendar.Component.VCALENDAR, null);
    ICalendar.Component child = new ICalendar.Component(
            ICalendar.Component.VEVENT, component);

    String tzid = //
    Utils.getSharedPreference(mContext,
            GeneralPreferences.KEY_HOME_TZ_ENABLED,
            false) ? //
    Utils.getSharedPreference(
            //
            mContext, GeneralPreferences.KEY_HOME_TZ,
            TimeZone.getDefault().getID()) : //
            TimeZone.getDefault().getID();

    ICalendar.Property dtstart_prop = new ICalendar.Property(
            "DTSTART",//
            new SimpleDateFormat("yyyyMMdd'T'HHmmss")
                    .format(mStartMillis));
    dtstart_prop.addParameter(new ICalendar.Parameter("TZID", tzid));
    child.addProperty(dtstart_prop);

    ICalendar.Property dtend_prop = new ICalendar.Property(
            "DTEND",//
            new SimpleDateFormat("yyyyMMdd'T'HHmmss")
                    .format(mEndMillis));
    dtend_prop.addParameter(new ICalendar.Parameter("TZID", tzid));
    child.addProperty(dtend_prop);

    child.addProperty(new ICalendar.Property("SUMMARY",
            mTitle.getText().toString()));
    child.addProperty(new ICalendar.Property(
            "LOCATION", mWhere.getText().toString()));
    child.addProperty(new ICalendar.Property(
            "DISCRIPTION", mDesc.getText().toString()));

    component.addChild(child);
    Log.d("info_action_share", component.toString());
```

导入时，同样使用`ICalendar`类，
```java
    event_title = c.getFirstProperty("SUMMARY").getValue();

    ICalendar.Property dtstart_prop = c.getFirstProperty("DTSTART");
    ICalendar.Property dtend_prop = c.getFirstProperty("DTEND");
    event_tz = dtstart_prop.getFirstParameter("TZID").value;
    SimpleDateFormat simpleDateFormat = new SimpleDateFormat(
            "yyyyMMdd'T'HHmmss");
    try {
        event_datetime = simpleDateFormat.parse(dtstart_prop.getValue())
                .getTime();
        event_dateendtime = simpleDateFormat.parse(dtend_prop.getValue())
                .getTime();
    } catch (ParseException e) {
        e.printStackTrace();
    }

    event_where = child.getFirstProperty("LOCATION").getValue();
    event_disc = child.getFirstProperty("DISCRIPTION").getValue();
```

保存日程，
```java
    ContentValues event = new ContentValues();
    event.put("title", event_title);
    event.put("description", event_disc);
    event.put("eventLocation", event_where);
    event.put("calendar_id", calId);
    event.put("dtstart", event_datetime);
    event.put("dtend", event_dateendtime);
    event.put("hasAlarm", 1);
    event.put("eventTimezone", event_tz);
    event.put("eventStatus", 1);
    Uri newEvent = getContentResolver().insert(
            Uri.parse("content://com.android.calendar/events"), event);
```

### 其他

其他还做了很多修改，暂时还不便给出，以后有机会会放到github上。














