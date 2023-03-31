@echo off
set rundate=
if NOT [%1] == [] (
  set rundate=%1
)
if [%1] == [] (
  set rundate=%date:~-4,4%%date:~-10,2%%date:~-7,2%
  echo [INFO] No date parameter provided, using today's date
)
echo [INFO] Using date: %rundate%

if exist Capture
echo [INFO] Running file validation...
if exist I:\BackupProd\Actionbuilderfiles\ActionBuilderNew\ActionBuilderFile-orgtx_%rundate%.TXT (echo [INFO] found file orgtx_%rundate%.txt) else (echo [ERROR] File not found orgtx_%rundate%.txt & goto nofile)
if exist I:\BackupProd\Actionbuilderfiles\ActionBuilderNew\ActionBuilderFile-00067_%rundate%.TXT (echo [INFO] found file 00067_%rundate%.txt) else (echo [ERROR] File not found 00067_%rundate%.txt & goto nofile)
if exist I:\BackupProd\Actionbuilderfiles\ActionBuilderNew\ActionBuilderFile-02048_%rundate%.TXT (echo [INFO] found file 02048_%rundate%.txt) else (echo [ERROR] File not found 02048_%rundate%.txt & goto nofile)
if exist I:\BackupProd\Actionbuilderfiles\ActionBuilderNew\ActionBuilderFile-03456_%rundate%.TXT (echo [INFO] found file 03456_%rundate%.txt) else (echo [ERROR] File not found 03456_%rundate%.txt & goto nofile)
if exist I:\BackupProd\Actionbuilderfiles\ActionBuilderNew\ActionBuilderFile-04518_%rundate%.TXT (echo [INFO] found file 04518_%rundate%.txt) else (echo [ERROR] File not found 04518_%rundate%.txt & goto nofile)
if exist I:\BackupProd\Actionbuilderfiles\ActionBuilderNew\ActionBuilderFile-06249_%rundate%.TXT (echo [INFO] found file 06249_%rundate%.txt) else (echo [ERROR] File not found 06249_%rundate%.txt & goto nofile)
if exist I:\BackupProd\Actionbuilderfiles\ActionBuilderNew\ActionBuilderFile-06448_%rundate%.TXT (echo [INFO] found file 06448_%rundate%.txt) else (echo [ERROR] File not found 06448_%rundate%.txt & goto nofile)
if exist I:\BackupProd\Actionbuilderfiles\ActionBuilderNew\ActionBuilderFile-06568_%rundate%.TXT (echo [INFO] found file 06568_%rundate%.txt) else (echo [ERROR] File not found 06568_%rundate%.txt & goto nofile)
if exist I:\BackupProd\Actionbuilderfiles\ActionBuilderNew\ActionBuilderFile-06198_%rundate%.TXT (echo [INFO] found file 06198_%rundate%.txt) else (echo [ERROR] File not found 06198_%rundate%.txt & goto nofile)
if exist I:\BackupProd\Actionbuilderfiles\ActionBuilderNew\ActionBuilderFile-08041_%rundate%.TXT (echo [INFO] found file 08041_%rundate%.txt) else (echo [ERROR] File not found 08041_%rundate%.txt & goto nofile)
echo [INFO] 10/10 files found

echo [INFO] DRY RUN: will not upload s3 files &
echo [INFO] Beginning s3api upload...
::aws s3api put-object --bucket ab-uploader-aft-uploads --key ActionBuilderFile-orgtx_%rundate%.txt --body I:\BackupProd\Actionbuilderfiles\ActionBuilderNew\ActionBuilderFile-orgtx_%rundate%.txt --acl "bucket-owner-full-control
::aws s3api put-object --bucket ab-uploader-aft-uploads --key ActionBuilderFile-00067_%rundate%.txt --body I:\BackupProd\Actionbuilderfiles\ActionBuilderNew\ActionBuilderFile-00067_%rundate%.txt --acl "bucket-owner-full-control
::aws s3api put-object --bucket ab-uploader-aft-uploads --key ActionBuilderFile-02048_%rundate%.txt --body I:\BackupProd\Actionbuilderfiles\ActionBuilderNew\ActionBuilderFile-02048_%rundate%.txt --acl "bucket-owner-full-control
::aws s3api put-object --bucket ab-uploader-aft-uploads --key ActionBuilderFile-03456_%rundate%.txt --body I:\BackupProd\Actionbuilderfiles\ActionBuilderNew\ActionBuilderFile-03456_%rundate%.txt --acl "bucket-owner-full-control
::aws s3api put-object --bucket ab-uploader-aft-uploads --key ActionBuilderFile-04518_%rundate%.txt --body I:\BackupProd\Actionbuilderfiles\ActionBuilderNew\ActionBuilderFile-04518_%rundate%.txt --acl "bucket-owner-full-control
::aws s3api put-object --bucket ab-uploader-aft-uploads --key ActionBuilderFile-06249_%rundate%.txt --body I:\BackupProd\Actionbuilderfiles\ActionBuilderNew\ActionBuilderFile-06249_%rundate%.txt --acl "bucket-owner-full-control
::aws s3api put-object --bucket ab-uploader-aft-uploads --key ActionBuilderFile-06448_%rundate%.txt --body I:\BackupProd\Actionbuilderfiles\ActionBuilderNew\ActionBuilderFile-06448_%rundate%.txt --acl "bucket-owner-full-control
::aws s3api put-object --bucket ab-uploader-aft-uploads --key ActionBuilderFile-06568_%rundate%.txt --body I:\BackupProd\Actionbuilderfiles\ActionBuilderNew\ActionBuilderFile-06568_%rundate%.txt --acl "bucket-owner-full-control
::aws s3api put-object --bucket ab-uploader-aft-uploads --key ActionBuilderFile-06198_%rundate%.txt --body I:\BackupProd\Actionbuilderfiles\ActionBuilderNew\ActionBuilderFile-06198_%rundate%.txt --acl "bucket-owner-full-control
::aws s3api put-object --bucket ab-uploader-aft-uploads --key ActionBuilderFile-08041_%rundate%.txt --body I:\BackupProd\Actionbuilderfiles\ActionBuilderNew\ActionBuilderFile-08041_%rundate%.txt --acl "bucket-owner-full-control

goto success

:success
  echo [INFO] File uploaded successfully!
  exit /b

:nofile
  echo [ERROR] Missing files, script exitting...
  exit /b

