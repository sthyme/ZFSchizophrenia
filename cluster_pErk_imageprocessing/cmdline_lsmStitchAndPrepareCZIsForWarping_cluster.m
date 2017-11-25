offset = 1; // use this to add to the 'fish number' output in the file name

setBatchMode(true); //doesn't show images, much faster
run("Bio-Formats Macro Extensions");

cmdoptions = getArgument;
print (cmdoptions);
cmdoptionssplit = split(cmdoptions," ");
FilePrefix = cmdoptionssplit[0]
target_dir = cmdoptionssplit[1]
ysize = cmdoptionssplit[2]
print (FilePrefix);
print (target_dir);
print (ysize);

//filestring = File.openAsString(cmdoptions);
//rows = split(filestring,"\n");

//FilePrefix_line = split(rows[0],"=");
//target_dir_line = split(rows[1],"=");
//size_line = split(rows[2],"=");

//FilePrefix = FilePrefix_line[1];
//target_dir = target_dir_line[1];
//ysize = size_line[1];


	//source_file = target_dir + list[i];
	//i = 0;
	source_file = target_dir + FilePrefix;
	print (source_file);
	saveNamelist = split(source_file, ".");
	saveName0 = saveNamelist[0];
	print (saveName0);
	run("Bio-Formats Importer", "open='"+ source_file +"' color_mode=Default view=Hyperstack stack_order=XYCZT  series_1");
	rename("Tile1");

	run("Bio-Formats Importer", "open='"+ source_file +"' color_mode=Default view=Hyperstack stack_order=XYCZT series_2");
	rename("Tile2");

	getVoxelSize(width, height, depth, unit);

	run("Pairwise stitching", "first_image='"+"Tile1"+"' second_image='"+"Tile2"+"' fusion_method=[Linear Blending] check_peaks=5 x=0.0000 y=ysize z=0 registration_channel_image_1=[Average all channels] registration_channel_image_2=[Average all channels]");

	setVoxelSize(width, height, depth, unit);


  rename("StitchedTiles"); //
	run("Split Channels");

	//saveName0 = split(source_file, ".")[0];
	//print (saveName0);

if (nImages == 6) { // four channels plus the original two images
		selectWindow("C4-StitchedTiles"); // select the X Channel

		//saveName = target_dir + FilePrefix + toString(i+offset) + "_04.nrrd"; // assign Y suffix number
		saveName = saveName0 + "_04.nrrd";

		run("Nrrd ... ", "nrrd=[saveName]");
		close();

		selectWindow("C3-StitchedTiles"); // select the X Channel

		//saveName = target_dir + FilePrefix + toString(i+offset) + "_01.nrrd"; // assign Y suffix number
		saveName = saveName0 + "_01.nrrd";

		run("Nrrd ... ", "nrrd=[saveName]");
		close();

		selectWindow("C2-StitchedTiles");

		//saveName = target_dir + FilePrefix + toString(i+offset) + "_02.nrrd";
		saveName = saveName0 + "_02.nrrd";

		run("Nrrd ... ", "nrrd=[saveName]");
		close();

		selectWindow("C1-StitchedTiles");

		//saveName = target_dir + FilePrefix + toString(i+offset) + "_03.nrrd";
		saveName = saveName0 + "_03.nrrd";

		run("Nrrd ... ", "nrrd=[saveName]");
		close();
		}
	else if (nImages == 5) { // three channels plus the original two OIBs

		selectWindow("C3-StitchedTiles"); // select the X Channel

		//saveName = target_dir + FilePrefix + toString(i+offset) + "_01.nrrd"; // assign Y suffix number
		saveName = saveName0 + "_01.nrrd";

		run("Nrrd ... ", "nrrd=[saveName]");
		close();

		selectWindow("C2-StitchedTiles");

		//saveName = target_dir + FilePrefix + toString(i+offset) + "_02.nrrd";
		saveName = saveName0 + "_02.nrrd";

		run("Nrrd ... ", "nrrd=[saveName]");
		close();

		selectWindow("C1-StitchedTiles");

		//saveName = target_dir + FilePrefix + toString(i+offset) + "_03.nrrd";
		saveName = saveName0 + "_03.nrrd";

		run("Nrrd ... ", "nrrd=[saveName]");
		close();
		}
	else if (nImages == 4){

		selectWindow("C2-StitchedTiles");

		//saveName = target_dir + FilePrefix + toString(i+offset) + "_01.nrrd";
		saveName = saveName0 + "_01.nrrd";

		run("Nrrd ... ", "nrrd=[saveName]");
		close();

		selectWindow("C1-StitchedTiles");

		//saveName = target_dir + FilePrefix + toString(i+offset) + "_02.nrrd";
		saveName = saveName0 + "_02.nrrd";

		run("Nrrd ... ", "nrrd=[saveName]");
		close();



	}
	else{
		exit("ERROR: not a 2, 3 or 4 channel image");
	}

	while (nImages > 0){
		close();
		}
	run("Collect Garbage");

//setBatchMode(false);
