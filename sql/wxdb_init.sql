-- ----------------------------
--  Sequence structure for robot_ai_config_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."robot_ai_config_id_seq";
CREATE SEQUENCE "public"."robot_ai_config_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."robot_ai_config_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for robot_wx_chat_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."robot_wx_chat_id_seq";
CREATE SEQUENCE "public"."robot_wx_chat_id_seq" INCREMENT 1 START 32 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."robot_wx_chat_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for robot_wx_hosting_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."robot_wx_hosting_id_seq";
CREATE SEQUENCE "public"."robot_wx_hosting_id_seq" INCREMENT 1 START 2 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."robot_wx_hosting_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for robot_wx_living_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."robot_wx_living_id_seq";
CREATE SEQUENCE "public"."robot_wx_living_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."robot_wx_living_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for wx_contact_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."wx_contact_id_seq";
CREATE SEQUENCE "public"."wx_contact_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."wx_contact_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for wx_msg_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."wx_msg_id_seq";
CREATE SEQUENCE "public"."wx_msg_id_seq" INCREMENT 1 START 159 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."wx_msg_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for wx_synckey_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."wx_synckey_id_seq";
CREATE SEQUENCE "public"."wx_synckey_id_seq" INCREMENT 1 START 36 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."wx_synckey_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Sequence structure for wx_user_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."wx_user_id_seq";
CREATE SEQUENCE "public"."wx_user_id_seq" INCREMENT 1 START 1 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "public"."wx_user_id_seq" OWNER TO "postgres";

-- ----------------------------
--  Table structure for wx_synckey
-- ----------------------------
DROP TABLE IF EXISTS "public"."wx_synckey";
CREATE TABLE "public"."wx_synckey" (
	"id" int8 NOT NULL DEFAULT nextval('wx_synckey_id_seq'::regclass),
	"device_id" varchar(50) COLLATE "default",
	"uin" varchar(50) COLLATE "default",
	"sid" varchar(100) COLLATE "default",
	"skey" varchar(100) COLLATE "default",
	"pass_ticket" varchar(100) COLLATE "default",
	"uuid" varchar COLLATE "default",
	"created_time" timestamp(6) WITH TIME ZONE,
	"synckey" varchar(500) COLLATE "default",
	"jsonsync" varchar(500) COLLATE "default",
	"updated_time" timestamp(6) WITH TIME ZONE,
	"username" varchar(100) COLLATE "default",
	"error_code" varchar(20) COLLATE "default",
	"exited_time" timestamp(6) WITH TIME ZONE,
	"cookie" varchar(2000) COLLATE "default",
	"base_uri" varchar(100) COLLATE "default"
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."wx_synckey" OWNER TO "postgres";

-- ----------------------------
--  Table structure for robot_wx_chat
-- ----------------------------
DROP TABLE IF EXISTS "public"."robot_wx_chat";
CREATE TABLE "public"."robot_wx_chat" (
	"id" int4 NOT NULL DEFAULT nextval('robot_wx_chat_id_seq'::regclass),
	"hosting_id" int8,
	"wx_uin" varchar(100) COLLATE "default",
	"type" varchar(20) COLLATE "default",
	"msg_id" varchar(100) COLLATE "default",
	"refer_id" varchar(100) COLLATE "default",
	"from_id" varchar(100) COLLATE "default",
	"from_name" varchar(100) COLLATE "default",
	"to_id" varchar(100) COLLATE "default",
	"to_name" varchar(100) COLLATE "default",
	"room_id" varchar(100) COLLATE "default",
	"room_name" varchar(100) COLLATE "default",
	"msg_type" varchar(20) COLLATE "default",
	"msg_content" varchar(2000) COLLATE "default",
	"msg_file" varchar(100) COLLATE "default",
	"msg_other" varchar(2000) COLLATE "default",
	"updated_time" timestamp(6) WITH TIME ZONE
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."robot_wx_chat" OWNER TO "postgres";

-- ----------------------------
--  Table structure for robot_ai_config
-- ----------------------------
DROP TABLE IF EXISTS "public"."robot_ai_config";
CREATE TABLE "public"."robot_ai_config" (
	"id" int4 NOT NULL DEFAULT nextval('robot_ai_config_id_seq'::regclass),
	"ai_num" varchar(50) COLLATE "default",
	"ai_props" json,
	"ai_tags" json,
	"status" int2,
	"updated_time" timestamp(6) WITH TIME ZONE
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."robot_ai_config" OWNER TO "postgres";

-- ----------------------------
--  Table structure for robot_wx_living
-- ----------------------------
DROP TABLE IF EXISTS "public"."robot_wx_living";
CREATE TABLE "public"."robot_wx_living" (
	"id" int4 NOT NULL DEFAULT nextval('robot_wx_living_id_seq'::regclass),
	"account" varchar(50) COLLATE "default",
	"living_type" varchar(20) COLLATE "default",
	"living_num" varchar(50) COLLATE "default",
	"living_title" varchar(50) COLLATE "default",
	"living_desc" varchar(500) COLLATE "default",
	"chatroom_id" varchar(50) COLLATE "default",
	"chatroom_name" varchar(50) COLLATE "default",
	"anchor" varchar(100) COLLATE "default",
	"hosting_id" int8,
	"hosting_uin" varchar(50) COLLATE "default",
	"status" int2 DEFAULT 1,
	"created_time" timestamp(6) WITH TIME ZONE,
	"updated_time" timestamp(6) WITH TIME ZONE,
	"start_time" timestamp(6) WITH TIME ZONE,
	"end_time" timestamp(6) WITH TIME ZONE,
	"remarks" varchar(255) COLLATE "default"
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."robot_wx_living" OWNER TO "postgres";

-- ----------------------------
--  Table structure for wx_user
-- ----------------------------
DROP TABLE IF EXISTS "public"."wx_user";
CREATE TABLE "public"."wx_user" (
	"id" int4 NOT NULL DEFAULT nextval('wx_user_id_seq'::regclass),
	"Uin" varchar(50) COLLATE "default",
	"UserName" varchar(50) COLLATE "default",
	"NickName" varchar(50) COLLATE "default",
	"Sex" varchar(10) COLLATE "default",
	"HeadImg" varchar(100) COLLATE "default",
	"jsonInfo" jsonb,
	"jsonTag" jsonb,
	"updated_time" timestamp(6) WITH TIME ZONE
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."wx_user" OWNER TO "postgres";

COMMENT ON COLUMN "public"."wx_user"."jsonInfo" IS '用户信息';
COMMENT ON COLUMN "public"."wx_user"."jsonTag" IS '用户标签';

-- ----------------------------
--  Table structure for robot_wx_hosting
-- ----------------------------
DROP TABLE IF EXISTS "public"."robot_wx_hosting";
CREATE TABLE "public"."robot_wx_hosting" (
	"id" int4 NOT NULL DEFAULT nextval('robot_wx_hosting_id_seq'::regclass),
	"account" varchar(50) COLLATE "default",
	"type" varchar(20) COLLATE "default",
	"device_server" varchar(50) COLLATE "default",
	"device_id" varchar(50) COLLATE "default",
	"wx_uin" varchar(50) COLLATE "default",
	"wx_name" varchar(50) COLLATE "default",
	"wx_props" json,
	"wx_cookie" varchar(500) COLLATE "default",
	"hosting_props" json,
	"ai_num" varchar(20) COLLATE "default",
	"status" int2 DEFAULT 1,
	"created_time" timestamp(6) WITH TIME ZONE,
	"updated_time" timestamp(6) WITH TIME ZONE,
	"remarks" varchar(255) COLLATE "default",
	"priority" int2 DEFAULT 0
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."robot_wx_hosting" OWNER TO "postgres";

-- ----------------------------
--  Table structure for wx_msg
-- ----------------------------
DROP TABLE IF EXISTS "public"."wx_msg";
CREATE TABLE "public"."wx_msg" (
	"id" int4 NOT NULL DEFAULT nextval('wx_msg_id_seq'::regclass),
	"uin" varchar(50) COLLATE "default",
	"msgid" varchar(50) COLLATE "default",
	"jsonmsg" jsonb,
	"updated_time" timestamp(6) WITH TIME ZONE
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."wx_msg" OWNER TO "postgres";

COMMENT ON COLUMN "public"."wx_msg"."uin" IS '用户信息';
COMMENT ON COLUMN "public"."wx_msg"."msgid" IS '消息ID';
COMMENT ON COLUMN "public"."wx_msg"."jsonmsg" IS '消息内容';

-- ----------------------------
--  Table structure for wx_contact
-- ----------------------------
DROP TABLE IF EXISTS "public"."wx_contact";
CREATE TABLE "public"."wx_contact" (
	"id" int4 NOT NULL DEFAULT nextval('wx_contact_id_seq'::regclass),
	"OwnerUin" varchar(50) COLLATE "default",
	"Uin" varchar(50) COLLATE "default",
	"UserName" varchar(50) COLLATE "default",
	"NickName" varchar(50) COLLATE "default",
	"HeadImg" varchar(100) COLLATE "default",
	"Sex" varchar(10) COLLATE "default",
	"ContactFlag" varchar(10) COLLATE "default",
	"jsonContact" jsonb,
	"updated_time" timestamp(6) WITH TIME ZONE,
	"last_action" varchar(20) COLLATE "default"
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."wx_contact" OWNER TO "postgres";

COMMENT ON COLUMN "public"."wx_contact"."OwnerUin" IS '微信用户';
COMMENT ON COLUMN "public"."wx_contact"."Uin" IS '联系人';
COMMENT ON COLUMN "public"."wx_contact"."ContactFlag" IS '联系人类型';
COMMENT ON COLUMN "public"."wx_contact"."jsonContact" IS '联系人信息';


-- ----------------------------
--  Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."robot_ai_config_id_seq" RESTART 2 OWNED BY "robot_ai_config"."id";
ALTER SEQUENCE "public"."robot_wx_chat_id_seq" RESTART 33 OWNED BY "robot_wx_chat"."id";
ALTER SEQUENCE "public"."robot_wx_hosting_id_seq" RESTART 3 OWNED BY "robot_wx_hosting"."id";
ALTER SEQUENCE "public"."robot_wx_living_id_seq" RESTART 2 OWNED BY "robot_wx_living"."id";
ALTER SEQUENCE "public"."wx_contact_id_seq" RESTART 2 OWNED BY "wx_contact"."id";
ALTER SEQUENCE "public"."wx_msg_id_seq" RESTART 160 OWNED BY "wx_msg"."id";
ALTER SEQUENCE "public"."wx_synckey_id_seq" RESTART 37 OWNED BY "wx_synckey"."id";
ALTER SEQUENCE "public"."wx_user_id_seq" RESTART 2 OWNED BY "wx_user"."id";
-- ----------------------------
--  Primary key structure for table wx_synckey
-- ----------------------------
ALTER TABLE "public"."wx_synckey" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table robot_wx_chat
-- ----------------------------
ALTER TABLE "public"."robot_wx_chat" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table robot_ai_config
-- ----------------------------
ALTER TABLE "public"."robot_ai_config" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table robot_wx_living
-- ----------------------------
ALTER TABLE "public"."robot_wx_living" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table wx_user
-- ----------------------------
ALTER TABLE "public"."wx_user" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table robot_wx_hosting
-- ----------------------------
ALTER TABLE "public"."robot_wx_hosting" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table wx_msg
-- ----------------------------
ALTER TABLE "public"."wx_msg" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Primary key structure for table wx_contact
-- ----------------------------
ALTER TABLE "public"."wx_contact" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

