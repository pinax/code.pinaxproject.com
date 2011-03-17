### New Model: notification.NoticeType
CREATE TABLE "notification_noticetype" (
    "id" serial NOT NULL PRIMARY KEY,
    "label" varchar(40) NOT NULL,
    "display" varchar(50) NOT NULL,
    "description" varchar(100) NOT NULL,
    "default" integer NOT NULL
)
;
### New Model: notification.NoticeSetting
CREATE TABLE "notification_noticesetting" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "notice_type_id" integer NOT NULL REFERENCES "notification_noticetype" ("id") DEFERRABLE INITIALLY DEFERRED,
    "medium" varchar(1) NOT NULL,
    "send" boolean NOT NULL,
    UNIQUE ("user_id", "notice_type_id", "medium")
)
;
### New Model: notification.NoticeQueueBatch
CREATE TABLE "notification_noticequeuebatch" (
    "id" serial NOT NULL PRIMARY KEY,
    "pickled_data" text NOT NULL
)
;
CREATE INDEX "notification_noticesetting_user_id" ON "notification_noticesetting" ("user_id");
CREATE INDEX "notification_noticesetting_notice_type_id" ON "notification_noticesetting" ("notice_type_id");
