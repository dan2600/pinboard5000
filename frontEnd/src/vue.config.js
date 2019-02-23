module.exports = {
	 configureWebpack: {
		entry: {
			app: './main.js',
		},
		optimization: {
			splitChunks: {
				chunks: 'all'
			}
		}
	}
}