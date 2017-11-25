max = 255; // set the max value of the images here - either 65535 for uint16, or 4096 if uint12 mapped

setBatchMode(true);

//source_dir = getArgument;
//target_dir = source_dir;

cmdoptions = getArgument;
//print (cmdoptions);
cmdoptionssplit = split(cmdoptions," ");
FilePrefix = cmdoptionssplit[0]
FileSuffix = cmdoptionssplit[1]
target_dir = cmdoptionssplit[2]
//print (FilePrefix);
//print (target_dir);
//print (ysize);

source_file = target_dir + FilePrefix + "_01_" + FileSuffix;
print (source_file);
saveNamelist = split(source_file, ".");
saveName0 = saveNamelist[0];
open(source_file);
run("Size...", "width=300 depth=80 constrain average interpolation=Bilinear");
       run("Gaussian Blur...", "sigma=2 stack");
       setMinAndMax(0, max);
	run("8-bit");
	saveAs("tiff", target_dir + "/" + FilePrefix + "_01_" + FileSuffix + "GauSmooth.tiff");
	close();
source_file = target_dir + FilePrefix + "_02_" + FileSuffix;
print (source_file);
saveNamelist = split(source_file, ".");
saveName0 = saveNamelist[0];
open(source_file);
run("Size...", "width=300 depth=80 constrain average interpolation=Bilinear");
       run("Gaussian Blur...", "sigma=2 stack");
       setMinAndMax(0, max);
	run("8-bit");
	saveAs("tiff", target_dir + "/" + FilePrefix + "_02_" + FileSuffix + "GauSmooth.tiff");
	close();
source_file = target_dir + FilePrefix + "_03_" + FileSuffix;
print (source_file);
saveNamelist = split(source_file, ".");
saveName0 = saveNamelist[0];
open(source_file);
run("Size...", "width=300 depth=80 constrain average interpolation=Bilinear");
       run("Gaussian Blur...", "sigma=2 stack");
       setMinAndMax(0, max);
	run("8-bit");
	saveAs("tiff", target_dir + "/" + FilePrefix + "_03_" + FileSuffix + "GauSmooth.tiff");
	close();
run("Collect Garbage");
