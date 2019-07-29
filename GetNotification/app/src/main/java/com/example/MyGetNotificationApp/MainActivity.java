package com.example.MyGetNotificationApp;

import android.content.Intent;
import android.database.Cursor;
import android.database.SQLException;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;


public class MainActivity extends AppCompatActivity {
    MyDBAdapter db = new MyDBAdapter(this);
    TextView t1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Log.i("Start", "Application Started");
        startActivity(new Intent("android.settings.ACTION_NOTIFICATION_LISTENER_SETTINGS"));
        startService(new Intent(MainActivity.this, GetNotificationService.class));

        t1 = (TextView) findViewById(R.id.textView);
        Button b1 = (Button)findViewById(R.id.button);
        b1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                try{
                    db.open();
                    String text = "";
                    Cursor c = db.fetchAllRecords();
                    c.moveToFirst();
                    while (c.moveToNext()){
                        text += c.getString(c.getColumnIndex("Content")) + "\n";
                    }
                    t1.setText(text);
                    c.close();
                    db.close();
                   /* c.moveToLast();
                    t1.setText(c.getString(c.getColumnIndex("Content")));*/
                    /*
                    try{
                        URL url = new URL("toutatis.cs.uiowa.edu");
                        HttpURLConnection conn = (HttpURLConnection)url.openConnection();
                        conn.setDoOutput(true);
                        conn.setRequestMethod("POST");
                        conn.setRequestProperty("Content-Type", "application/json");
                        conn.connect();
                    } catch (MalformedURLException e){

                    }*/

                } catch(Exception e){
                    t1.setText("Something went wrong");
                }
            }
        });
    }



}



