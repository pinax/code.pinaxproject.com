### New Model: tasks.PinnedList_tasks
CREATE TABLE "tasks_pinnedlist_tasks" (
    "id" serial NOT NULL PRIMARY KEY,
    "pinnedlist_id" integer NOT NULL,
    "task_id" integer NOT NULL REFERENCES "tasks_task" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("pinnedlist_id", "task_id")
)
;
### New Model: tasks.PinnedList
CREATE TABLE "tasks_pinnedlist" (
    "id" serial NOT NULL PRIMARY KEY,
    "created_by_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_on" timestamp with time zone NOT NULL,
    "name" varchar(256)
)
;
ALTER TABLE "tasks_pinnedlist_tasks" ADD CONSTRAINT "pinnedlist_id_refs_id_2a59ec44" FOREIGN KEY ("pinnedlist_id") REFERENCES "tasks_pinnedlist" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "tasks_pinnedlist_tasks_pinnedlist_id" ON "tasks_pinnedlist_tasks" ("pinnedlist_id");
CREATE INDEX "tasks_pinnedlist_tasks_task_id" ON "tasks_pinnedlist_tasks" ("task_id");
CREATE INDEX "tasks_pinnedlist_created_by_id" ON "tasks_pinnedlist" ("created_by_id");
