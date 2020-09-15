module.exports = {
    entry: 'index.js',
    css: {
       extract: true
    },
    output: {
        fileNames: {
            js: 'site.js',
            css: 'site.css'
        },
        format: 'umd',
        moduleName: 'site'
    }
};