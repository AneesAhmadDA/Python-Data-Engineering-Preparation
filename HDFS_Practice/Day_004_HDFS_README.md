# Day 004 --- HDFS Fundamentals and File Operations

## Learning Objectives

-   Inspect the HDFS root directory.
-   Check cluster health with `hdfs dfsadmin -report`.
-   Create HDFS directories.
-   Copy a Windows file into a Docker container and upload it to HDFS.
-   Read a file stored in HDFS.
-   Inspect HDFS blocks and replication.

## Environment

  Component                 Configuration
  ------------------------- --------------------------
  Hadoop image              `apache/hadoop:3.4.1`
  NameNode container        `hdfs-lab-namenode`
  DataNode container        `hdfs-lab-datanode`
  NameNode web UI           `http://localhost:19870`
  DataNode web UI           `http://localhost:19864`
  Replication factor        `1`
  HDFS practice directory   `/tmp/day004_hdfs_lab`

This is a single-DataNode learning environment, not a production-grade
distributed cluster.

## Task 1 --- Inspect the HDFS Cluster

### List the HDFS root

``` powershell
docker exec -it hdfs-lab-namenode hdfs dfs -ls /
```

The root listing was empty at the time of inspection. An empty listing
produces no file or directory rows.

### Check cluster health

``` powershell
docker exec -it hdfs-lab-namenode hdfs dfsadmin -report
```

Observed report:

  Metric                  Observed value
  --------------------- ----------------
  Configured capacity         1006.85 GB
  Present capacity             932.86 GB
  DFS remaining                932.86 GB
  DFS used                         24 KB
  Live DataNodes                       1
  Missing blocks                       0
  Corrupt replicas                     0

The report confirmed one live DataNode and no missing blocks or corrupt
replicas.

## Task 2 --- Create an HDFS Directory

Create the practice directory:

``` powershell
docker exec -it hdfs-lab-namenode hdfs dfs -mkdir -p /tmp/day004_hdfs_lab
```

Verify it:

``` powershell
docker exec -it hdfs-lab-namenode hdfs dfs -ls /tmp
```

`-mkdir` creates a directory. `-p` creates missing parent directories
and does not fail if the target directory already exists.

## Task 3 --- Upload a Local File to HDFS

First, check that the local sample file exists from the `HDFS_Practice`
project directory:

``` powershell
Get-ChildItem .\sample_data\
```

Copy it from Windows into the NameNode container:

``` powershell
docker cp .\sample_data\sample.txt hdfs-lab-namenode:/tmp/sample.txt
```

**Important:** `docker cp` places the file in the container's local
filesystem. It does not upload the file into HDFS.

Upload the container-local file into HDFS:

``` powershell
docker exec -it hdfs-lab-namenode hdfs dfs -put /tmp/sample.txt /tmp/day004_hdfs_lab/
```

Verify the HDFS file:

``` powershell
docker exec -it hdfs-lab-namenode hdfs dfs -ls /tmp/day004_hdfs_lab
```

`hdfs dfs -put` transfers a local file into HDFS.

## Task 4 --- Read the HDFS File

``` powershell
docker exec -it hdfs-lab-namenode hdfs dfs -cat /tmp/day004_hdfs_lab/sample.txt
```

`hdfs dfs -cat` prints the contents of the file stored in HDFS to the
terminal.

## Task 5 --- Inspect Blocks and Replication

Run these follow-up commands and record their actual outputs.

Inspect file blocks and their locations:

``` powershell
docker exec -it hdfs-lab-namenode hdfs fsck /tmp/day004_hdfs_lab/sample.txt -files -blocks -locations
```

Check the replication factor:

``` powershell
docker exec -it hdfs-lab-namenode hdfs dfs -getrep /tmp/day004_hdfs_lab/sample.txt
```

The lab is configured with replication factor `1`; use the command
output to verify the file's actual replication.

## Key Concepts

  -----------------------------------------------------------------------
  Concept                             Explanation
  ----------------------------------- -----------------------------------
  NameNode                            Manages filesystem metadata,
                                      including directories, filenames,
                                      permissions, and block locations.

  DataNode                            Stores the actual HDFS data blocks.

  HDFS root (`/`)                     Root of the HDFS filesystem;
                                      separate from the Windows
                                      filesystem.

  `hdfs dfs -mkdir`                   Creates directories in HDFS.

  `docker cp`                         Copies files between the host and a
                                      container's local filesystem.

  `hdfs dfs -put`                     Uploads a local file into HDFS.

  `hdfs dfs -cat`                     Displays the contents of an HDFS
                                      file.

  HDFS blocks                         Units into which HDFS divides files
                                      for storage.

  Replication factor                  Number of copies configured for
                                      each HDFS block.
  -----------------------------------------------------------------------

## Completion Checklist

-   [x] Inspected the HDFS root directory.
-   [x] Checked the HDFS cluster report.
-   [x] Confirmed one live DataNode.
-   [x] Created `/tmp/day004_hdfs_lab`.
-   [x] Copied the sample file into the NameNode container.
-   [x] Uploaded `sample.txt` into HDFS.
-   [x] Read the HDFS file using `hdfs dfs -cat`.
-   [ ] Inspected file blocks and locations using `hdfs fsck`.
-   [ ] Verified replication using `hdfs dfs -getrep`.

Only mark the final two items complete after running and reviewing those
commands.

## Important Notes

-   This HDFS learning lab is separate from the Ambulance Intelligence
    capstone.
-   Avoid `docker compose down -v` for routine cleanup because it
    removes named volumes and can delete stored HDFS data.
-   One DataNode with replication factor 1 is appropriate for this
    exercise, but does not demonstrate fault-tolerant multi-node
    replication.
