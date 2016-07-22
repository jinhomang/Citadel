TrexConfig.addTool(
	"shcode",
	{
		wysiwygonly: _TRUE,
		sync: _FALSE,
		status: _FALSE
	}
);

TrexMessage.addMsg({
	'@shcode.title': "소스코드",
});
	
Trex.Tool.Shcode = Trex.Class.create({
	$const: {
		__Identity: 'shcode'
	},
	$extend: Trex.Tool,
	oninitialized: function() {
		var _editor = this.editor;
		this.weave.bind(this)(
			new Trex.Button(this.buttonCfg), 
			_NULL,
			function() {
				_editor.getSidebar().getEmbeder("shcode").execute();
			}
		);
	}
});

TrexConfig.addEmbeder(
	"shcode",
	{
		wysiwygonly: _TRUE,
		useCC: _FALSE,
		features: {
			left:250, 
			top:65, 
			width:458, 
			height:568,
			resizable:"yes"
		},
		popPageUrl: "#host#path/pages/trex/syntaxhighlightcode.html",
		allowNetworkingFilter: _FALSE,
		allowNetworkingSites: []
	},
	function(root) {
		var _config = root.sidebar.embeder.shcode; 
		_config.popPageUrl = TrexConfig.getUrl(_config.popPageUrl);
		_config.features = TrexConfig.getPopFeatures(_config.features);
	}
);

(function() {

	Trex.Embeder.ShCode = Trex.Class.create({
		$const: {
			__Identity: 'shcode'
		},
		$extend: Trex.Embeder,
		name: 'shcode',
		title: TXMSG("@shcode.title"),
		canResized: _TRUE,
		getCreatedHtml: function(data){
			return data;
			// data.code || this.makeSourceByUrl(data.url);
			// return convertToHtml(_source);
		}
	});

	Trex.register("filter > shcode ", function(editor, toolbar, sidebar){
		//var _config = sidebar.embeders.media.config;
		editor.getDocParser().registerFilter('filter/embeder/media', {
			'text@load': function(contents){
				return contents;
			}
		});
	});	
		
})();
