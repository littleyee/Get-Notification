BEGIN TRANSACTION;
CREATE TABLE Notification_Table ( Package VARCHAR(255), Title VARCHAR(255), Content VARCHAR(255), TimeStamp VARCHAR(255), Location VARCHAR(255) );
INSERT INTO "Notification_Table" VALUES('com.google.android.apps.messaging','4','message4','1564576418256','Chicago');
INSERT INTO "Notification_Table" VALUES('com.google.android.apps.messaging','3','message3','1564576418279','Chicago');
INSERT INTO "Notification_Table" VALUES('com.google.android.apps.messaging','2','message2','1564576418310','Chicago');
INSERT INTO "Notification_Table" VALUES('com.google.android.apps.messaging','1','message1','1564576418338','Chicago');
COMMIT;