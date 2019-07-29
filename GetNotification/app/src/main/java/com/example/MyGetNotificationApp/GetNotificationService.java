package com.example.MyGetNotificationApp;

import android.annotation.SuppressLint;
import android.app.Notification;
import android.content.Context;
import android.database.SQLException;
import android.os.Build;
import android.os.Bundle;
import android.os.RemoteException;
import android.service.notification.NotificationListenerService;
import android.service.notification.StatusBarNotification;
import android.util.Log;

import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;


@SuppressLint("OverrideAbstract")
public class GetNotificationService extends NotificationListenerService {

    MyDBAdapter db = new MyDBAdapter(this);
	// Declare database helper object
	// i.e. MyDBHelper mDB;
    Context context;
//    @Override
//    public void onCreate(){
//        super.onCreate();
//        context = getApplicationContext();
//        Log.i("Service Start", "GNS created as a service");
//		// Open/Create the Database
//		// i.e. mDB.open();
//        try{
//            db.open();
//        } catch(SQLException e){
//            Log.e("SQLException","Error opening database");
//        }
//
//    }


    @Override
    public void onNotificationPosted(StatusBarNotification sbn) {
        Log.i("Notification Found", "Notification was posted");
        Notification notification = sbn.getNotification();

        if (null == notification) {
            return;
        }

        context = getApplicationContext();
        Log.i("Service Start", "GNS created as a service");
		// Open/Create the Database
		// i.e. mDB.open();
        try{
            db.open();
        } catch(SQLException e){
            Log.e("SQLException","Error opening database");
        }

        //To get details of notification through extras if API > 18
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
            Bundle extras = notification.extras;

            if (extras != null) {
                //get package name
                String pack = sbn.getPackageName();

                //get package posted time
                String timestamp = Long.toString(sbn.getPostTime());

                //get title of notification
                String title = extras.getString(Notification.EXTRA_TITLE, "");
                //get content of notification
                String content = extras.getString(Notification.EXTRA_TEXT, "");
                //get ticker of notification

                Log.d("Package: ", pack);
                Log.d("PostedTime: ", timestamp);

                Log.d("Title: ", title);
                Log.d("Content: ", content);

                db.createRecord(pack, title, content, timestamp);

                Log.d("Query Test", db.fetchpack(pack, title, content, timestamp));

				
				//Add the notification data to an entry
			//mDB.addNotification(title, pack, content ...);


            }
    }

        db.close();
    }
}
