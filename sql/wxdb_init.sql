CREATE TABLE "public"."wx_hosting" (
	"id" int8 NOT NULL,
	"user" varchar(50),
	"type" varchar(20),
	"status" varchar(20),
	"wx_uid" varchar(50),
	"wx_name" varchar(50),
	"wx_props" varchar(255),
	"device_id" varchar(50),
	"wx_cookie" varchar(255),
	"hosting_props" varchar(255),
	"created_time" timestamptz,
	"updated_time" timestamptz,
	"enabled" int2,
	"remarks" varchar(255),
	PRIMARY KEY ("id")
)
WITH (OIDS=FALSE);