# ソースファイル

source_data フォルダに、 https://ita.ee.lbl.gov/html/contrib/NASA-HTTP.html　から `NASA_access_log_Jul95.gz` をダウンロードして保存する。

# sqlmesh からどのように database が見えているかを確認する方法

sqlmesh fetchdf で、 information_schema をクエリする。

> uv run sqlmesh fetchdf "select * from information_schema.schemata"

# duckdb で、catalog に登録したローカルdbへのクエリ方法

ローカルdb に直接接続しても、「catalog が見つからない」というエラーが出てしまう。

```
duckdb ./data/local_data_mart.duckdb
DuckDB v1.4.2 (Andium) 68d7555f68
Enter ".help" for usage hints.
D select * from information_schema.schemata;
┌─────────────────┬────────────────────┬──────────────┬───────────────────────────────┬──────────────────────────────┬────────────────────────────┬──────────┐
│  catalog_name   │    schema_name     │ schema_owner │ default_character_set_catalog │ default_character_set_schema │ default_character_set_name │ sql_path │
│     varchar     │      varchar       │   varchar    │            varchar            │           varchar            │          varchar           │ varchar  │
├─────────────────┼────────────────────┼──────────────┼───────────────────────────────┼──────────────────────────────┼────────────────────────────┼──────────┤
│ local_data_mart │ main               │ duckdb       │ NULL                          │ NULL                         │ NULL                       │ NULL     │
│ local_data_mart │ sqlmesh__summary   │ duckdb       │ NULL                          │ NULL                         │ NULL                       │ NULL     │
│ local_data_mart │ summary            │ duckdb       │ NULL                          │ NULL                         │ NULL                       │ NULL     │
│ system          │ information_schema │ duckdb       │ NULL                          │ NULL                         │ NULL                       │ NULL     │
│ system          │ main               │ duckdb       │ NULL                          │ NULL                         │ NULL                       │ NULL     │
│ system          │ pg_catalog         │ duckdb       │ NULL                          │ NULL                         │ NULL                       │ NULL     │
│ temp            │ main               │ duckdb       │ NULL                          │ NULL                         │ NULL                       │ NULL     │
└─────────────────┴────────────────────┴──────────────┴───────────────────────────────┴──────────────────────────────┴────────────────────────────┴──────────┘
D select * from information_schema.tables;
┌─────────────────┬──────────────────┬──────────────────────┬────────────┬──────────────────────┬──────────────────────┬───┬──────────────────────┬──────────────────────┬────────────────────┬──────────┬───────────────┬───────────────┐
│  table_catalog  │   table_schema   │      table_name      │ table_type │ self_referencing_c…  │ reference_generation │ … │ user_defined_type_…  │ user_defined_type_…  │ is_insertable_into │ is_typed │ commit_action │ TABLE_COMMENT │
│     varchar     │     varchar      │       varchar        │  varchar   │       varchar        │       varchar        │   │       varchar        │       varchar        │      varchar       │ varchar  │    varchar    │    varchar    │
├─────────────────┼──────────────────┼──────────────────────┼────────────┼──────────────────────┼──────────────────────┼───┼──────────────────────┼──────────────────────┼────────────────────┼──────────┼───────────────┼───────────────┤
│ local_data_mart │ sqlmesh__summary │ summary__kennedy_s…  │ BASE TABLE │ NULL                 │ NULL                 │ … │ NULL                 │ NULL                 │ YES                │ NO       │ NULL          │ NULL          │
│ local_data_mart │ summary          │ kennedy_space_center │ VIEW       │ NULL                 │ NULL                 │ … │ NULL                 │ NULL                 │ NO                 │ NO       │ NULL          │ NULL          │
├─────────────────┴──────────────────┴──────────────────────┴────────────┴──────────────────────┴──────────────────────┴───┴──────────────────────┴──────────────────────┴────────────────────┴──────────┴───────────────┴───────────────┤
│ 2 rows                                                                                                                                                                                                           13 columns (12 shown) │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
D select * from local_data_mart.summary.kennedy_space_center;
Binder Error:
Catalog "persistent" does not exist!
```

オンメモリのduckdbを立ち上げて、アタッチすると参照できるようになる。

```
 duckdb                              
DuckDB v1.4.2 (Andium) 68d7555f68
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
D ATTACH './data/local_data_mart.duckdb' as persistent;
D select * from information_schema.schemata;
┌──────────────┬────────────────────┬──────────────┬───────────────────────────────┬──────────────────────────────┬────────────────────────────┬──────────┐
│ catalog_name │    schema_name     │ schema_owner │ default_character_set_catalog │ default_character_set_schema │ default_character_set_name │ sql_path │
│   varchar    │      varchar       │   varchar    │            varchar            │           varchar            │          varchar           │ varchar  │
├──────────────┼────────────────────┼──────────────┼───────────────────────────────┼──────────────────────────────┼────────────────────────────┼──────────┤
│ memory       │ main               │ duckdb       │ NULL                          │ NULL                         │ NULL                       │ NULL     │
│ persistent   │ main               │ duckdb       │ NULL                          │ NULL                         │ NULL                       │ NULL     │
│ persistent   │ sqlmesh__summary   │ duckdb       │ NULL                          │ NULL                         │ NULL                       │ NULL     │
│ persistent   │ summary            │ duckdb       │ NULL                          │ NULL                         │ NULL                       │ NULL     │
│ system       │ information_schema │ duckdb       │ NULL                          │ NULL                         │ NULL                       │ NULL     │
│ system       │ main               │ duckdb       │ NULL                          │ NULL                         │ NULL                       │ NULL     │
│ system       │ pg_catalog         │ duckdb       │ NULL                          │ NULL                         │ NULL                       │ NULL     │
│ temp         │ main               │ duckdb       │ NULL                          │ NULL                         │ NULL                       │ NULL     │
└──────────────┴────────────────────┴──────────────┴───────────────────────────────┴──────────────────────────────┴────────────────────────────┴──────────┘
D select * from information_schema.tables;
┌───────────────┬──────────────────┬──────────────────────┬────────────┬──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬───────────────────────┬────────────────────┬──────────┬───────────────┬───────────────┐
│ table_catalog │   table_schema   │      table_name      │ table_type │ self_referencing_c…  │ reference_generation │ user_defined_type_…  │ user_defined_type_…  │ user_defined_type_n…  │ is_insertable_into │ is_typed │ commit_action │ TABLE_COMMENT │
│    varchar    │     varchar      │       varchar        │  varchar   │       varchar        │       varchar        │       varchar        │       varchar        │        varchar        │      varchar       │ varchar  │    varchar    │    varchar    │
├───────────────┼──────────────────┼──────────────────────┼────────────┼──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼───────────────────────┼────────────────────┼──────────┼───────────────┼───────────────┤
│ persistent    │ sqlmesh__summary │ summary__kennedy_s…  │ BASE TABLE │ NULL                 │ NULL                 │ NULL                 │ NULL                 │ NULL                  │ YES                │ NO       │ NULL          │ NULL          │
│ persistent    │ summary          │ kennedy_space_center │ VIEW       │ NULL                 │ NULL                 │ NULL                 │ NULL                 │ NULL                  │ NO                 │ NO       │ NULL          │ NULL          │
└───────────────┴──────────────────┴──────────────────────┴────────────┴──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴───────────────────────┴────────────────────┴──────────┴───────────────┴───────────────┘
D select * from persistent.summary.kennedy_space_center;
┌──────────────────────────┬────────────────────────────────────┬──────────────────────────┬─────────┬─────────────────────────────────────────────────────┬──────────┬────────┬───────┐
│       access_date        │                host                │           time           │ method  │                        path                         │ protocol │ status │ size  │
│ timestamp with time zone │              varchar               │ timestamp with time zone │ varchar │                       varchar                       │ varchar  │ int64  │ int64 │
├──────────────────────────┼────────────────────────────────────┼──────────────────────────┼─────────┼─────────────────────────────────────────────────────┼──────────┼────────┼───────┤
│ 1995-07-01 13:00:00+09   │ mozart.forest.dnj.ynu.ac.jp        │ 1995-07-02 05:27:12+09   │ GET     │ /images/ksclogo-medium.gif                          │ HTTP/1.0 │    200 │  5866 │
│ 1995-07-01 13:00:00+09   │ mozart.forest.dnj.ynu.ac.jp        │ 1995-07-02 05:27:13+09   │ GET     │ /images/MOSAIC-logosmall.gif                        │ HTTP/1.0 │    200 │   363 │
│ 1995-07-01 13:00:00+09   │ mozart.forest.dnj.ynu.ac.jp        │ 1995-07-02 05:27:13+09   │ GET     │ /images/NASA-logosmall.gif                          │ HTTP/1.0 │    200 │   786 │
│ 1995-07-01 13:00:00+09   │ mozart.forest.dnj.ynu.ac.jp        │ 1995-07-02 05:27:13+09   │ GET     │ /images/USA-logosmall.gif                           │ HTTP/1.0 │    200 │   234 │
│ 1995-07-01 13:00:00+09   │ mozart.forest.dnj.ynu.ac.jp        │ 1995-07-02 05:27:13+09   │ GET     │ /images/WORLD-logosmall.gif                         │ HTTP/1.0 │    200 │   669 │
│ 1995-07-01 13:00:00+09   │ dial33.ppp.iastate.edu             │ 1995-07-02 05:27:13+09   │ GET     │ /                                                   │ HTTP/1.0 │    200 │  7074 │
│ 1995-07-01 13:00:00+09   │ 129.130.80.122                     │ 1995-07-02 05:27:14+09   │ GET     │ /shuttle/missions/sts-71/images/KSC-95EC-0913.gif   │ HTTP/1.0 │    200 │ 21957 │
│ 1995-07-01 13:00:00+09   │ n106.napa.community.net            │ 1995-07-02 05:27:15+09   │ GET     │ /shuttle/technology/images/et-intertank_1-small.gif │ HTTP/1.0 │    200 │ 65536 │
│ 1995-07-01 13:00:00+09   │ dial33.ppp.iastate.edu             │ 1995-07-02 05:27:15+09   │ GET     │ /images/ksclogo-medium.gif                          │ HTTP/1.0 │    200 │  5866 │
│ 1995-07-01 13:00:00+09   │ dial33.ppp.iastate.edu             │ 1995-07-02 05:27:17+09   │ GET     │ /images/NASA-logosmall.gif                          │ HTTP/1.0 │    200 │   786 │
│ 1995-07-01 13:00:00+09   │ dial33.ppp.iastate.edu             │ 1995-07-02 05:27:17+09   │ GET     │ /images/MOSAIC-logosmall.gif                        │ HTTP/1.0 │    200 │   363 │
│ 1995-07-01 13:00:00+09   │ dial33.ppp.iastate.edu             │ 1995-07-02 05:27:18+09   │ GET     │ /images/USA-logosmall.gif                           │ HTTP/1.0 │    200 │   234 │
│ 1995-07-01 13:00:00+09   │ 142.170.43.6                       │ 1995-07-02 05:27:19+09   │ GET     │ /shuttle/countdown/                                 │ HTTP/1.0 │    200 │  3985 │
│ 1995-07-01 13:00:00+09   │ www-proxy.crl.research.digital.com │ 1995-07-02 05:27:19+09   │ GET     │ /shuttle/countdown/lps/fr.html                      │ HTTP/1.0 │    200 │  1879 │
│ 1995-07-01 13:00:00+09   │ dial33.ppp.iastate.edu             │ 1995-07-02 05:27:20+09   │ GET     │ /images/WORLD-logosmall.gif                         │ HTTP/1.0 │    200 │   669 │
│ 1995-07-01 13:00:00+09   │ www-proxy.crl.research.digital.com │ 1995-07-02 05:27:20+09   │ GET     │ /shuttle/countdown/lps/fr.gif                       │ HTTP/1.0 │    200 │ 30232 │
│ 1995-07-01 13:00:00+09   │ www-proxy.crl.research.digital.com │ 1995-07-02 05:27:20+09   │ GET     │ /shuttle/countdown/lps/back.gif                     │ HTTP/1.0 │    200 │  1289 │
│ 1995-07-01 13:00:00+09   │ pm1-11.abc.se                      │ 1995-07-02 05:27:21+09   │ GET     │ /shuttle/missions/sts-68/sts-68-patch-small.gif     │ HTTP/1.0 │    200 │ 17459 │
│ 1995-07-01 13:00:00+09   │ ix-phx4-13.ix.netcom.com           │ 1995-07-02 05:27:22+09   │ GET     │ /images/NASA-logosmall.gif                          │ HTTP/1.0 │    304 │     0 │
│ 1995-07-01 13:00:00+09   │ ix-phx4-13.ix.netcom.com           │ 1995-07-02 05:27:23+09   │ GET     │ /images/KSC-logosmall.gif                           │ HTTP/1.0 │    304 │     0 │
│           ·              │      ·                             │           ·              │  ·      │            ·                                        │    ·     │     ·  │     · │
│           ·              │      ·                             │           ·              │  ·      │            ·                                        │    ·     │     ·  │     · │
│           ·              │      ·                             │           ·              │  ·      │            ·                                        │    ·     │     ·  │     · │
│ 1995-07-28 13:00:00+09   │ aa27.bc.edu                        │ 1995-07-29 01:22:40+09   │ GET     │ /images/kscmap-small.gif                            │ HTTP/1.0 │    200 │ 39017 │
│ 1995-07-28 13:00:00+09   │ web.kyoto-inet.or.jp               │ 1995-07-29 01:22:40+09   │ GET     │ /shuttle/missions/sts-70/images/KSC-95EC-0635.gif   │ HTTP/1.0 │    200 │ 43551 │
│ 1995-07-28 13:00:00+09   │ aa27.bc.edu                        │ 1995-07-29 01:22:40+09   │ GET     │ /images/KSC-logosmall.gif                           │ HTTP/1.0 │    200 │  1204 │
│ 1995-07-28 13:00:00+09   │ pcmas.it.bton.ac.uk                │ 1995-07-29 01:22:42+09   │ GET     │ /htbin/cdt_clock.pl                                 │ HTTP/1.0 │    200 │   503 │
│ 1995-07-28 13:00:00+09   │ onet2.cup.hp.com                   │ 1995-07-29 01:22:44+09   │ GET     │ /images/                                            │ HTTP/1.0 │    200 │ 17688 │
│ 1995-07-28 13:00:00+09   │ alumni1.newcollege.utoronto.ca     │ 1995-07-29 01:22:44+09   │ GET     │ /history/apollo/apollo.html                         │ HTTP/1.0 │    200 │  3260 │
│ 1995-07-28 13:00:00+09   │ alumni1.newcollege.utoronto.ca     │ 1995-07-29 01:22:46+09   │ GET     │ /history/apollo/images/footprint-small.gif          │ HTTP/1.0 │    200 │ 18149 │
│ 1995-07-28 13:00:00+09   │ onet2.cup.hp.com                   │ 1995-07-29 01:22:47+09   │ GET     │ /icons/blank.xbm                                    │ HTTP/1.0 │    200 │   509 │
│ 1995-07-28 13:00:00+09   │ dialup552.chicago.mci.net          │ 1995-07-29 01:22:48+09   │ GET     │ /images/launchmedium.gif                            │ HTTP/1.0 │    200 │ 11853 │
│ 1995-07-28 13:00:00+09   │ sdn_b6_f02_ip.dny.rockwell.com     │ 1995-07-29 01:22:50+09   │ GET     │ /history/apollo/apollo-13/movies/                   │ HTTP/1.0 │    200 │   945 │
│ 1995-07-28 13:00:00+09   │ sanders.jsc.nasa.gov               │ 1995-07-29 01:22:50+09   │ GET     │ /shuttle/missions/                                  │ HTTP/1.0 │    200 │ 12283 │
│ 1995-07-28 13:00:00+09   │ onet2.cup.hp.com                   │ 1995-07-29 01:22:55+09   │ GET     │ /icons/menu.xbm                                     │ HTTP/1.0 │    200 │   527 │
│ 1995-07-28 13:00:00+09   │ torquay.sms.co.uk                  │ 1995-07-29 01:22:55+09   │ GET     │ /shuttle/countdown/                                 │ HTTP/1.0 │    200 │  4324 │
│ 1995-07-28 13:00:00+09   │ sdn_b6_f02_ip.dny.rockwell.com     │ 1995-07-29 01:22:55+09   │ GET     │ /icons/blank.xbm                                    │ HTTP/1.0 │    200 │   509 │
│ 1995-07-28 13:00:00+09   │ sdn_b6_f02_ip.dny.rockwell.com     │ 1995-07-29 01:22:56+09   │ GET     │ /icons/movie.xbm                                    │ HTTP/1.0 │    200 │   530 │
│ 1995-07-28 13:00:00+09   │ onet2.cup.hp.com                   │ 1995-07-29 01:22:57+09   │ GET     │ /icons/image.xbm                                    │ HTTP/1.0 │    200 │   509 │
│ 1995-07-28 13:00:00+09   │ sanders.jsc.nasa.gov               │ 1995-07-29 01:22:58+09   │ GET     │ /icons/text.xbm                                     │ HTTP/1.0 │    200 │   527 │
│ 1995-07-28 13:00:00+09   │ sdn_b6_f02_ip.dny.rockwell.com     │ 1995-07-29 01:22:59+09   │ GET     │ /icons/menu.xbm                                     │ HTTP/1.0 │    200 │   527 │
│ 1995-07-28 13:00:00+09   │ 158.111.42.17                      │ 1995-07-29 01:23:00+09   │ GET     │ /history/apollo/apollo-1/apollo-1.html              │ HTTP/1.0 │    200 │  3841 │
│ 1995-07-28 13:00:00+09   │ onet2.cup.hp.com                   │ 1995-07-29 01:23:00+09   │ GET     │ /icons/unknown.xbm                                  │ HTTP/1.0 │    200 │   515 │
├──────────────────────────┴────────────────────────────────────┴──────────────────────────┴─────────┴─────────────────────────────────────────────────────┴──────────┴────────┴───────┤
│ 1869103 rows (1.87 million rows, 40 shown)                                                                                                                                 8 columns │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
