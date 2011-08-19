### New Model: voting.Vote
CREATE TABLE "votes" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
    "object_id" integer CHECK ("object_id" >= 0) NOT NULL,
    "vote" smallint NOT NULL,
    UNIQUE ("user_id", "content_type_id", "object_id")
)
;
CREATE INDEX "votes_user_id" ON "votes" ("user_id");
CREATE INDEX "votes_content_type_id" ON "votes" ("content_type_id");
