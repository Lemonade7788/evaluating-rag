-- Calendar definition

CREATE TABLE "Calendar" (
	"year" INTEGER,
	"month" TEXT,
	"day" TEXT,
	english_date INTEGER,
	chinese_date INTEGER,
	muslim_date INTEGER,
	moon_phases TEXT,
	events TEXT,
	kuching_high_water_1 TEXT,
	kuching_high_water_2 TEXT,
	miri_high_water_1 TEXT,
	miri_high_water_2 TEXT,
	miri_high_water_3 TEXT
);


-- ImportExport1969 definition

CREATE TABLE "ImportExport1969" (
	district VARCHAR,
	"import_dollar" INTEGER,
	"export_dollar" INTEGER,
	"year" INTEGER
);


-- KapitAdminTransfer1970 definition

CREATE TABLE KapitAdminTransfer1970 (
	name VARCHAR,
	"rank" VARCHAR,
	"transfer_from" VARCHAR,
	"transfer_to" VARCHAR,
	"effective_date" NVARCHAR,
	remarks VARCHAR,
	"year" INTEGER,
	district VARCHAR
);


-- KuchingMarketPrice definition

CREATE TABLE "KuchingMarketPrice" (
	"year" INTEGER,
	"month" TEXT(50),
	category VARCHAR(50),
	item VARCHAR(50),
	per VARCHAR(50),
	average_price NUMERIC
);


-- LunduEntranceExam definition

CREATE TABLE LunduEntranceExam (
	"year" INTEGER,
	no_of_pupils INTEGER,
	selected INTEGER,
	percent INTEGER,
	district VARCHAR(50)
);


-- PrimarySchoolDropouts definition

CREATE TABLE "PrimarySchoolDropouts" (
	cohort_beginning INTEGER,
	std_1_count INTEGER,
	std_1_retention_rate INTEGER,
	std_2_count INTEGER,
	std_2_retention_rate INTEGER,
	std_3_count INTEGER,
	std_3_retention_rate INTEGER,
	std_4_count INTEGER,
	std_4_retention_rate INTEGER,
	std_5_count INTEGER,
	std_5_retention_rate INTEGER,
	std_6_count INTEGER,
	std_6_retention_rate INTEGER,
	state VARCHAR
);


-- SarawakFinance definition

CREATE TABLE "SarawakFinance" (
	"year" INTEGER,
	"revenue_dollar" INTEGER,
	"expenditure_dollar" INTEGER,
	state VARCHAR
);