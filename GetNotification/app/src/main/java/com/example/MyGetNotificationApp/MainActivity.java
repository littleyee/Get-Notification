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
                    Cursor c = db.fetchAllRecords();
                    c.moveToLast();
                    t1.setText(c.getString(c.getColumnIndex("Content")));

                } catch(Exception e){
                    t1.setText("Something went wrong");
                }
            }
        });
    }



}



