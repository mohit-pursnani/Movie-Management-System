DROP TABLE IF EXISTS Revenue CASCADE;
DROP TABLE IF EXISTS Movie CASCADE;
DROP TABLE IF EXISTS Casts CASCADE;
DROP TABLE IF EXISTS Director CASCADE;
DROP TABLE IF EXISTS Producer CASCADE;
DROP TABLE IF EXISTS Genre CASCADE;
DROP TABLE IF EXISTS Award CASCADE;
DROP TABLE IF EXISTS Theater CASCADE;
DROP TABLE IF EXISTS Show CASCADE;
DROP TABLE IF EXISTS StreamingPlatform CASCADE;
DROP TABLE IF EXISTS Viewer CASCADE;
DROP TABLE IF EXISTS Viewed_Rated_by CASCADE;
DROP TABLE IF EXISTS Movie_belong_to CASCADE;
DROP TABLE IF EXISTS Directed_by CASCADE;
DROP TABLE IF EXISTS Produced_by CASCADE;
DROP TABLE IF EXISTS Starred_by CASCADE;
DROP TABLE IF EXISTS Streamed_On CASCADE;
DROP TABLE IF EXISTS Played_At CASCADE;
DROP TABLE IF EXISTS Receive_Awards CASCADE;


CREATE TABLE Revenue (
  Id Integer Primary Key, 
  TotalExpense bigint not null,
  TotalEarnings bigint not null,
  CollectedRevenue bigint GENERATED ALWAYS AS (TotalEarnings-TotalExpense)STORED
);

CREATE TABLE Movie (
  Id integer Primary Key,
  Name varchar(100) not null,
  Language varchar(100),
  Country varchar(100),
  Release_date Date not null,
  Length Integer not null,
  Revenue_Id Integer not null,
  FOREIGN KEY(Revenue_Id) references Revenue(Id)
 );

CREATE TABLE Casts (
  Id integer Primary Key,
  Name varchar(100) not null,
  Age Integer,
  Gender varchar(10)
 );

CREATE TABLE Director (
  Id integer Primary Key,
  Name varchar(100) not null,
  Age Integer,
  Gender varchar(10)
 );

CREATE TABLE Producer (
  Id integer Primary Key,
  Name varchar(100) not null,
  Age Integer,
  Gender varchar(10)
 );

CREATE TABLE Genre (
  Id integer Primary Key,
  Type varchar(128)
);

 CREATE TABLE Award (
  Id integer Primary Key,
  Type varchar(500)
);

CREATE TABLE Theater (
  Id Integer Primary Key, 
  Name varchar(100) not null,
  ZIP_Code Integer
);

CREATE TABLE Show (
  Id Integer, 
  Theater_Id Integer,
  S_Date Date not null,
  S_Time time not null,
  Primary Key(Theater_Id, Id),
  FOREIGN KEY(Theater_Id) references Theater(Id) on delete cascade
);

CREATE TABLE StreamingPlatform(
  Id Integer Primary Key,
  Name varchar(100) not null
 );


CREATE TABLE Viewer(
  Id Integer Primary Key,
  Name varchar(100) not null,
  Age Integer, 
  Gender varchar(10)
 );

CREATE TABLE Viewed_Rated_by(
  Viewer_Id Integer, 
  Movie_Id Integer,
  Rating Float,
  Primary Key(Viewer_Id, Movie_Id),
  Foreign Key(Movie_Id) references Movie(Id),
  Foreign Key(Viewer_Id) references Viewer(Id)
 );


CREATE TABLE Movie_belong_to(
  Genre_Id Integer, 
  Movie_Id Integer,
  Primary Key(Genre_Id, Movie_Id),
  Foreign Key(Movie_Id) references Movie(Id),
  Foreign Key(Genre_Id) references Genre(Id)
 );


CREATE TABLE Directed_by(
  Director_Id Integer, 
  Movie_Id Integer,
  Primary Key(Director_Id, Movie_Id),
  Foreign Key(Movie_Id) references Movie(Id),
  Foreign Key(Director_Id) references Director(Id)
 );
 
 CREATE TABLE Produced_by(
  Producer_Id Integer, 
  Movie_Id Integer,
  Primary Key(Producer_Id, Movie_Id),
  Foreign Key(Movie_Id) references Movie(Id),
  Foreign Key(Producer_Id) references Producer(Id)
 );

CREATE TABLE Starred_by(
  Cast_Id Integer, 
  Movie_Id Integer,
  Primary Key(Cast_Id, Movie_Id),
  Foreign Key(Movie_Id) references Movie(Id),
  Foreign Key(Cast_Id) references Casts(Id)
 );

 CREATE TABLE Streamed_On(
  Streaming_Platform_Id Integer, 
  Movie_Id Integer,
  Primary Key(Streaming_Platform_Id, Movie_Id),
  Foreign Key(Movie_Id) references Movie(Id),
  Foreign Key(Streaming_Platform_Id) references StreamingPlatform(Id)
 );

CREATE TABLE Played_At(
  Theater_Id Integer, 
  Movie_Id Integer,
  Primary Key(Theater_Id, Movie_Id),
  Foreign Key(Movie_Id) references Movie(Id),
  Foreign Key(Theater_Id) references Theater(Id)
 );
 
 CREATE TABLE Receive_Awards(
  Award_Id Integer,
  Year Integer,
  Movie_Id Integer,
  Primary Key(Award_Id, Movie_Id),
  Foreign Key(Award_Id) references Award(Id),
  Foreign Key(Movie_Id) references Movie(Id)
 );
