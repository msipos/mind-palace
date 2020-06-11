module.exports = {
    entry: 'index.js',
    output: {
        fileNames: {
            js: 'site.js',
            css: 'site.css'
        },
        format: 'umd',
        moduleName: 'site'
    }
};