Data stores to support - AWS S3, Google Drive, GCP
Operations to support:
1. add
2. status
3. push
4. RESET
5. pull

Config: File that describe the behavior - should be present on each of the
folder where we are planning on using the lib
@Props:
  1. DataStorage: ["S3" | "GoogDrive" | "GCP"]
  2. ShallowDepth: How many older versions to maintain for e.g. if set to 3 then we can only revert 3 steps
  3. ModificationIdentification: Mechanism to identify if a file is modified ["time" | "md5"]
  4. DataFolder: Folder where datasets are stored
  5. SupportedDataTypes: List containing the type of files you consider as a dataset ["csv", "tsv", ...]


RefFile: Maintains the history of commits, to be used to rollback if required
Cache: Contains the previous versions of files with a folder for each file, with file names being the commit hash value
