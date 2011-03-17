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
### New Model: notification.ObservedItem
CREATE TABLE "notification_observeditem" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
    "object_id" integer CHECK ("object_id" >= 0) NOT NULL,
    "notice_type_id" integer NOT NULL REFERENCES "notification_noticetype" ("id") DEFERRABLE INITIALLY DEFERRED,
    "added" timestamp with time zone NOT NULL,
    "signal" text NOT NULL
)
;
CREATE INDEX "notification_noticesetting_user_id" ON "notification_noticesetting" ("user_id");
CREATE INDEX "notification_noticesetting_notice_type_id" ON "notification_noticesetting" ("notice_type_id");
CREATE INDEX "notification_observeditem_user_id" ON "notification_observeditem" ("user_id");
CREATE INDEX "notification_observeditem_content_type_id" ON "notification_observeditem" ("content_type_id");
CREATE INDEX "notification_observeditem_notice_type_id" ON "notification_observeditem" ("notice_type_id");
