/**
 * Created by hyj on 2016/8/19.
 */
var webpack = require('webpack');
module.exports = {
    entry: [

        'webpack/hot/only-dev-server',
        "./src/main/app.js"
    ],
    output: {
        path: __dirname+"/build",
        filename: "bundle.js"
    },
    module: {
        loaders: [
            {
                test:/\.css$/,
                loader:"style!css"
            },{
                test:/\.(gif|jpg|png|woff|svg|eot|ttf)\??.*$/,
                loader:'url-loader?limit=50000&name=[path][name].[ext]'
            },{
                //test:/\.js?$/,loaders:['react-hot',"babel?presets[]=react,presets[]=es2015"],exclude: /node_modules/
                test: /\.js?$/,
                loaders:['react-hot',"babel?presets[]=react,presets[]=es2015"],
                exclude: /node_modules/
            }
        ]
    },
    resolve: {
        extensions: ['','.coffee','.js',',json']
    },
    plugins:[
        new webpack.NoErrorsPlugin()
    ],
    devtool: "cheap-module-eval-source-map"
}