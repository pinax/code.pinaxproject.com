### New Model: admin.LogEntry
CREATE TABLE "django_admin_log" (
    "id" serial NOT NULL PRIMARY KEY,
    "action_time" timestamp with time zone NOT NULL,
    "user_id" integer NOT NULL,
    "content_type_id" integer,
    "object_id" text,
    "object_repr" varchar(200) NOT NULL,
    "action_flag" smallint CHECK ("action_flag" >= 0) NOT NULL,
    "change_message" text NOT NULL
)
;
### New Model: auth.Permission
CREATE TABLE "auth_permission" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "content_type_id" integer NOT NULL,
    "codename" varchar(100) NOT NULL,
    UNIQUE ("content_type_id", "codename")
)
;
### New Model: auth.Group_permissions
CREATE TABLE "auth_group_permissions" (
    "id" serial NOT NULL PRIMARY KEY,
    "group_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("group_id", "permission_id")
)
;
### New Model: auth.Group
CREATE TABLE "auth_group" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(80) NOT NULL UNIQUE
)
;
ALTER TABLE "auth_group_permissions" ADD CONSTRAINT "group_id_refs_id_3cea63fe" FOREIGN KEY ("group_id") REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED;
### New Model: auth.User_user_permissions
CREATE TABLE "auth_user_user_permissions" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("user_id", "permission_id")
)
;
### New Model: auth.User_groups
CREATE TABLE "auth_user_groups" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("user_id", "group_id")
)
;
### New Model: auth.User
CREATE TABLE "auth_user" (
    "id" serial NOT NULL PRIMARY KEY,
    "username" varchar(30) NOT NULL UNIQUE,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL,
    "email" varchar(75) NOT NULL,
    "password" varchar(128) NOT NULL,
    "is_staff" boolean NOT NULL,
    "is_active" boolean NOT NULL,
    "is_superuser" boolean NOT NULL,
    "last_login" timestamp with time zone NOT NULL,
    "date_joined" timestamp with time zone NOT NULL
)
;
ALTER TABLE "django_admin_log" ADD CONSTRAINT "user_id_refs_id_c8665aa" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "auth_user_user_permissions" ADD CONSTRAINT "user_id_refs_id_f2045483" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "auth_user_groups" ADD CONSTRAINT "user_id_refs_id_831107f1" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
### New Model: auth.Message
CREATE TABLE "auth_message" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "message" text NOT NULL
)
;
### New Model: contenttypes.ContentType
CREATE TABLE "django_content_type" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "app_label" varchar(100) NOT NULL,
    "model" varchar(100) NOT NULL,
    UNIQUE ("app_label", "model")
)
;
ALTER TABLE "django_admin_log" ADD CONSTRAINT "content_type_id_refs_id_288599e6" FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "auth_permission" ADD CONSTRAINT "content_type_id_refs_id_728de91f" FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED;
### New Model: sessions.Session
CREATE TABLE "django_session" (
    "session_key" varchar(40) NOT NULL PRIMARY KEY,
    "session_data" text NOT NULL,
    "expire_date" timestamp with time zone NOT NULL
)
;
### New Model: sites.Site
CREATE TABLE "django_site" (
    "id" serial NOT NULL PRIMARY KEY,
    "domain" varchar(100) NOT NULL,
    "name" varchar(50) NOT NULL
)
;
### New Model: emailconfirmation.EmailAddress
CREATE TABLE "emailconfirmation_emailaddress" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "email" varchar(75) NOT NULL,
    "verified" boolean NOT NULL,
    "primary" boolean NOT NULL,
    UNIQUE ("user_id", "email")
)
;
### New Model: emailconfirmation.EmailConfirmation
CREATE TABLE "emailconfirmation_emailconfirmation" (
    "id" serial NOT NULL PRIMARY KEY,
    "email_address_id" integer NOT NULL REFERENCES "emailconfirmation_emailaddress" ("id") DEFERRABLE INITIALLY DEFERRED,
    "sent" timestamp with time zone NOT NULL,
    "confirmation_key" varchar(40) NOT NULL
)
;
### New Model: account.Account
CREATE TABLE "account_account" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "timezone" varchar(100) NOT NULL,
    "language" varchar(10) NOT NULL
)
;
### New Model: account.OtherServiceInfo
CREATE TABLE "account_otherserviceinfo" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "key" varchar(50) NOT NULL,
    "value" text NOT NULL,
    UNIQUE ("user_id", "key")
)
;
### New Model: account.PasswordReset
CREATE TABLE "account_passwordreset" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "temp_key" varchar(100) NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    "reset" boolean NOT NULL
)
;
### New Model: signup_codes.SignupCode
CREATE TABLE "signup_codes_signupcode" (
    "id" serial NOT NULL PRIMARY KEY,
    "code" varchar(40) NOT NULL,
    "max_uses" integer CHECK ("max_uses" >= 0) NOT NULL,
    "expiry" timestamp with time zone,
    "inviter_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "email" varchar(75) NOT NULL,
    "notes" text NOT NULL,
    "created" timestamp with time zone NOT NULL,
    "use_count" integer CHECK ("use_count" >= 0) NOT NULL
)
;
### New Model: signup_codes.SignupCodeResult
CREATE TABLE "signup_codes_signupcoderesult" (
    "id" serial NOT NULL PRIMARY KEY,
    "signup_code_id" integer NOT NULL REFERENCES "signup_codes_signupcode" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "timestamp" timestamp with time zone NOT NULL
)
;
### New Model: django_openid.Nonce
CREATE TABLE "django_openid_nonce" (
    "id" serial NOT NULL PRIMARY KEY,
    "server_url" varchar(255) NOT NULL,
    "timestamp" integer NOT NULL,
    "salt" varchar(40) NOT NULL
)
;
### New Model: django_openid.Association
CREATE TABLE "django_openid_association" (
    "id" serial NOT NULL PRIMARY KEY,
    "server_url" text NOT NULL,
    "handle" varchar(255) NOT NULL,
    "secret" text NOT NULL,
    "issued" integer NOT NULL,
    "lifetime" integer NOT NULL,
    "assoc_type" text NOT NULL
)
;
### New Model: django_openid.UserOpenidAssociation
CREATE TABLE "django_openid_useropenidassociation" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "openid" varchar(255) NOT NULL,
    "created" timestamp with time zone NOT NULL
)
;
CREATE INDEX "django_admin_log_user_id" ON "django_admin_log" ("user_id");
CREATE INDEX "django_admin_log_content_type_id" ON "django_admin_log" ("content_type_id");
CREATE INDEX "auth_permission_content_type_id" ON "auth_permission" ("content_type_id");
CREATE INDEX "auth_group_permissions_group_id" ON "auth_group_permissions" ("group_id");
CREATE INDEX "auth_group_permissions_permission_id" ON "auth_group_permissions" ("permission_id");
CREATE INDEX "auth_user_user_permissions_user_id" ON "auth_user_user_permissions" ("user_id");
CREATE INDEX "auth_user_user_permissions_permission_id" ON "auth_user_user_permissions" ("permission_id");
CREATE INDEX "auth_user_groups_user_id" ON "auth_user_groups" ("user_id");
CREATE INDEX "auth_user_groups_group_id" ON "auth_user_groups" ("group_id");
CREATE INDEX "auth_message_user_id" ON "auth_message" ("user_id");
CREATE INDEX "emailconfirmation_emailaddress_user_id" ON "emailconfirmation_emailaddress" ("user_id");
CREATE INDEX "emailconfirmation_emailconfirmation_email_address_id" ON "emailconfirmation_emailconfirmation" ("email_address_id");
CREATE INDEX "account_otherserviceinfo_user_id" ON "account_otherserviceinfo" ("user_id");
CREATE INDEX "account_passwordreset_user_id" ON "account_passwordreset" ("user_id");
CREATE INDEX "signup_codes_signupcode_inviter_id" ON "signup_codes_signupcode" ("inviter_id");
CREATE INDEX "signup_codes_signupcoderesult_signup_code_id" ON "signup_codes_signupcoderesult" ("signup_code_id");
CREATE INDEX "signup_codes_signupcoderesult_user_id" ON "signup_codes_signupcoderesult" ("user_id");
CREATE INDEX "django_openid_useropenidassociation_user_id" ON "django_openid_useropenidassociation" ("user_id");
