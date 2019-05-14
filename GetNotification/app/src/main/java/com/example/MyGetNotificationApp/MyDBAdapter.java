package com.example.MyGetNotificationApp;
import android.content.ContentValues;
import android.content.Context;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.database.Cursor;
import android.database.sqlite.SQLiteOpenHelper;
import android.util.Log;

public class MyDBAdapter {
    // Column names
    public static final String COLUMN_PACK = "Package";
    public static final String COLUMN_TITLE = "Title";
    public static final String COLUMN_CONTENT = "Content";


    //Indices
    public static final int INDEX_PACK = 0;
    public static final int INDEX_TITLE = 1;
    public static final int INDEX_CONTENT = 2;

    // create tag
    public static final String TAG = "RecordMyDBHelper";

    private DataBaseHelper myDbHelper;
    private SQLiteDatabase db;

    private static final int DATABASE_VERSION = 1;
    private static final String DATABASE_NAME = "Notification_Record";
    private static final String TABLE_NAME = "Notification_Table";

    private final Context mycontext;

    private static final String DATABASE_CREATE = "CREATE TABLE if not exists " + TABLE_NAME + " ( " +
            COLUMN_PACK + " VARCHAR(255), " +
            COLUMN_TITLE + " VARCHAR(255), " +
            COLUMN_CONTENT + " VARCHAR(255) );";


    public MyDBAdapter(Context mycontext) {

        this.mycontext = mycontext;
    }

    public void open() throws SQLException {
        myDbHelper = new DataBaseHelper(mycontext);
        db = myDbHelper.getWritableDatabase();
    }

    public void close() {
        if (myDbHelper != null) {
            myDbHelper.close();
        }
    }

    public void createRecord (String packname, String title, String content) {
        ContentValues values = new ContentValues();
        values.put(COLUMN_PACK, packname);
        values.put(COLUMN_TITLE, title);
        values.put(COLUMN_CONTENT, content);
        db.insert(TABLE_NAME, null, values);
    }

    public String fetchpack(String packname, String title, String content) {
        Cursor cursor = db.query(TABLE_NAME, new String[] {COLUMN_PACK},
                COLUMN_PACK + "=?",
                new String[] {String.valueOf(packname)},
                null, null, null);
        if(cursor != null) {
            cursor.moveToFirst();
        }
        return  "Packname = " + packname + " Title = " +  title + " Content = " + content;
    }

    public Cursor fetchAllRecords() {
        Cursor mycursor = db.query(TABLE_NAME, new String[]{COLUMN_PACK, COLUMN_TITLE, COLUMN_CONTENT},
                null, null, null, null, null);

        if(mycursor != null) {
            mycursor.moveToFirst();
        }

        return mycursor;
    }

    private static class DataBaseHelper extends SQLiteOpenHelper {
        public DataBaseHelper(Context context) {
            super(context, DATABASE_NAME, null, DATABASE_VERSION);
        }

        @Override
        public void onCreate(SQLiteDatabase db){
            Log.w(TAG, DATABASE_CREATE);
            db.execSQL(DATABASE_CREATE);
        }

        @Override
        public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
            Log.w(TAG, "Upgrading database from version " + oldVersion  + "to " + newVersion+
                    " which wil destroy all data");
            db.execSQL("DROP TABLE IF EXISTS " + TABLE_NAME);
            onCreate(db);
        }
    }
}

