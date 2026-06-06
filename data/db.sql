-- CalendarApril definition

CREATE TABLE CalendarApril (
	"year" TEXT,
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


-- CalendarAugust definition

CREATE TABLE CalendarAugust (
	"year" TEXT,
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


-- CalendarDecember definition

CREATE TABLE CalendarDecember (
	"year" TEXT,
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


-- CalendarFebruary definition

CREATE TABLE CalendarFebruary (
	"year" TEXT,
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


-- CalendarJanuary definition

CREATE TABLE "CalendarJanuary" (
	"year" TEXT,
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


-- CalendarJuly definition

CREATE TABLE CalendarJuly (
	"year" TEXT,
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


-- CalendarJune definition

CREATE TABLE CalendarJune (
	"year" TEXT,
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


-- CalendarMarch definition

CREATE TABLE CalendarMarch (
	"year" TEXT,
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


-- CalendarMay definition

CREATE TABLE CalendarMay (
	"year" TEXT,
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


-- CalendarNovember definition

CREATE TABLE CalendarNovember (
	"year" TEXT,
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


-- CalendarOctober definition

CREATE TABLE CalendarOctober (
	"year" TEXT,
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


-- CalendarSeptember definition

CREATE TABLE CalendarSeptember (
	"year" TEXT,
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

CREATE TABLE ImportExport1969 (
	District VARCHAR(50),
	"Import (dollar)" NVARCHAR(50),
	"Export (dollar)" NVARCHAR(50),
	"year" INTEGER
);


-- KapitAdminTransfer1970 definition

CREATE TABLE KapitAdminTransfer1970 (
	Name VARCHAR(50),
	"Rank" VARCHAR(128),
	"Transfer From" VARCHAR(50),
	"Transfer To" VARCHAR(50),
	"Effective Date" NVARCHAR(50),
	Remarks VARCHAR(64),
	"year" INTEGER,
	district VARCHAR(50)
);


-- KuchingMarketPriceApril1971 definition

CREATE TABLE "KuchingMarketPriceApril1971" (
"year" INTEGER,
  "month" TEXT,
  "category" TEXT,
  "item" TEXT,
  "per" TEXT,
  "average_price" REAL
);


-- KuchingMarketPriceJuly1971 definition

CREATE TABLE "KuchingMarketPriceJuly1971" (
"year" INTEGER,
  "month" TEXT,
  "category" TEXT,
  "item" TEXT,
  "per" TEXT,
  "average_price" REAL
);


-- KuchingMarketPriceJune1971 definition

CREATE TABLE "KuchingMarketPriceJune1971" (
"year" INTEGER,
  "month" TEXT,
  "category" TEXT,
  "item" TEXT,
  "per" TEXT,
  "average_price" REAL
);


-- KuchingMarketPriceMarch1971 definition

CREATE TABLE "KuchingMarketPriceMarch1971" (
"year" INTEGER,
  "month" TEXT,
  "category" TEXT,
  "item" TEXT,
  "per" TEXT,
  "average_price" REAL
);


-- KuchingMarketPriceNovember1970 definition

CREATE TABLE "KuchingMarketPriceNovember1970" (
"year" INTEGER,
  "month" TEXT,
  "category" TEXT,
  "item" TEXT,
  "per" TEXT,
  "average_price" REAL
);


-- KuchingMarketPriceNovember1971 definition

CREATE TABLE "KuchingMarketPriceNovember1971" (
"year" INTEGER,
  "month" TEXT,
  "category" TEXT,
  "item" TEXT,
  "per" TEXT,
  "average_price" REAL
);


-- LunduEntranceExam definition

CREATE TABLE LunduEntranceExam (
	"year" INTEGER,
	no_of_pupils INTEGER,
	selected INTEGER,
	percent INTEGER,
	district VARCHAR
);


-- Metadata definition

CREATE TABLE Metadata (
	table_name TEXT NOT NULL,
	description TEXT,
	CONSTRAINT Metadata_PK PRIMARY KEY (table_name)
);


-- PrimarySchoolDropouts definition

CREATE TABLE PrimarySchoolDropouts (
	cohort_beginning INTEGER,
	std_1_count NVARCHAR,
	std_1_retention_rate INTEGER,
	std_2_count NVARCHAR,
	std_2_retention_rate REAL,
	std_3_count NVARCHAR,
	std_3_retention_rate REAL,
	std_4_count NVARCHAR,
	std_4_retention_rate REAL,
	std_5_count NVARCHAR,
	std_5_retention_rate REAL,
	std_6_count NVARCHAR,
	std_6_retention_rate REAL,
	state VARCHAR
);


-- SarawakFinance definition

CREATE TABLE SarawakFinance (
	"Year" INTEGER,
	"Revenue (dollar)" NVARCHAR,
	"Expenditure (dollar)" NVARCHAR,
	state VARCHAR
);
