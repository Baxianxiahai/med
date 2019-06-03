Please install the Node.js v5.1.0 or higher (V10 or higher is recommended).
IF your environment have not install the gulp & webpack, u need install them first:
npm install gulp -g
npm install webpack -g
npm install -g node-gyp
npm install --global --production windows-build-tools

pay attention: these command may need administrator power.

Then add your npm node path into System PATH, and keep command "gulp" & "webpack" can run everywhere.

Change your work DIR to source folder.
Keep your internet link fluent, or you can use the set the npm mirror in your country.
1) Prepare the environment for node_modules, command:
npm install --save-dev

You may face some compile error under windows for MOSCA, it will be OK if your windows-build-tools install correctly.
2) build the source, command:
npm run build
#3) copy the useful resource to the deliver folder, command:
#gulp
#PHP may not support anymore
If u want to use NodeJS server instead of apache and PHP, u need to run extra command:
1) cd ./target_module
2) npm install --save-dev
3) cd ..
4) gulp jsserver
the 4) step will update the Node server's node_modules, and it will cost time. so if your environment already has the modules, u can just run
4) gulp jsupdate




If u want to change the gulp target, please edit the gulp file's content:
var option = {
    buildPath: "../www/zhmed"
}
var jsserverpath="../nodewww";

To your apache or node www path.

If u want to run the node server, goto your node www path and run the command:
node mqttserver.js
node launch.js

The mqttserver.js provide the mqtt Service and launch.js provide the httpd and mqttclient service.
The web also need to link mqttserver service in further plan.


before gulp, u can open the gulpfile.js as a text file, can modify some replace marco information.



U can get the output in fold /dist.

Directory structure:
----+-build         // save the js & resource file after they are built
    +-resource      // 3rd resource folder
    +-dist          // save the final deliver files
    +-node_modules  // Node.js plugin folder, all dependence will be save in it after npm install
    +-src           // source folder
    +-baseconf      // configure file for function
    +-demo          // demo picture for video
    +-icon          // icon svg folder
    +-language      // language folder
    +-sysconf       // configure file for system information
    +-userconf      // configure file for user information
    --gulpfile.js   // gulp command configuration
    --index.html    // entry of the UI, will be compiled
    --package.json  // npm configuration file
    --readme.txt    // help file
    --product_description.txt    // Production discription
    --request.php   // php entry for Apache&PHP environment
    --webpack.config.js //webpack react hot server configuration file
    --webpack.build.config.js //webpack build configuration file


.

before u open the web, go to the !src code! folder,run these command in 2 different command windows:
node mqttserver.js
node mqttclient.js

the server must be launched before client, and your sever's 1883/3000 port should be free.
