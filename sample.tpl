<!-- Google conversion -->
{if:!String.strcmp(#/index.php#,request.php_self)}
	<!-- Page d'accueil -->
	<script type="text/javascript">
		var google_tag_params = {
			ecomm_prodid: '',
			ecomm_pagetype: 'home',
			ecomm_totalvalue: ''
		};
	</script>
{else:}
	{if:!String.strcmp(#/catalog/product_one.php#,request.php_self)}
		{if:product.lowerPriceET}
			<!-- Fiche produit ayant un prix -->
			<flexy:toJavascript idproduct={product.id}></flexy:toJavascript>
			<flexy:toJavascript priceproduct={product.lowerPriceET}></flexy:toJavascript>
			<script type="text/javascript">
				var google_tag_params = {
					ecomm_prodid: idproduct,
					ecomm_pagetype: 'product',
					ecomm_totalvalue: priceproduct
				};
			</script>
		{else:}
			<!-- Fiche produit sans prix -->
			<flexy:toJavascript idproduct={product.id}></flexy:toJavascript>
			<script type="text/javascript">
				var google_tag_params = {
					ecomm_prodid: idproduct,
					ecomm_pagetype: 'product',
					ecomm_totalvalue: ''
				};
			</script>
		{end:}
	{else:}
		{if:!String.strcmp(#/catalog/product.php#,request.php_self)}
			{if:category.id}
				<!-- Catégories -->
				<flexy:toJavascript idcategory={category.id}></flexy:toJavascript>
				<script type="text/javascript">
					var google_tag_params = {
						ecomm_prodid: idcategory,
						ecomm_pagetype: 'category',
						ecomm_totalvalue: ''
					};
				</script>
			{else:}
				<!-- Toutes les autres pagesssss -->
				<script type="text/javascript">
					var google_tag_params = {
						ecomm_prodid: '',
						ecomm_pagetype: 'siteview',
						ecomm_totalvalue: ''
					};
				</script>
			{end:}
		{else:}
			{if:!String.strcmp(#/catalog/basket.php#,request.php_self)}
				<!-- Panier -->
				<flexy:toJavascript totalvaluebasket={basket.getTotalATI()}></flexy:toJavascript>
				{stack.reset()}
				{foreach:basket.items,item}
				    {stack.push(item.article.idproduct)}
				{end:}
				<flexy:toJavascript products={stack.toArray()}></flexy:toJavascript>

				<script type="text/javascript">
					var google_tag_params = {
						ecomm_prodid: products,
						ecomm_pagetype: 'cart',
						ecomm_totalvalue: totalvaluebasket
					};
				</script>
			{else:}
				<!-- Toutes les autres pages -->
				<script type="text/javascript">
					var google_tag_params = {
						ecomm_prodid: '',
						ecomm_pagetype: 'siteview',
						ecomm_totalvalue: ''
					};
				</script>
			{end:}
		{end:}
	{end:}
{end:}

<script type="text/javascript">
	var google_conversion_id = 1062519530;
	var google_conversion_label = "PQzRCLLHtAIQ6oXT-gM";
	var google_custom_params = window.google_tag_params;
	var google_remarketing_only = true;
</script>

<script async type="text/javascript" src="//www.googleadservices.com/pagead/conversion.js"></script>
<noscript>
	<div>
		<img height="1" width="1" alt="Google conversion" src="//www.google.fr/ads/conversion/1062519530/?value=0&amp;label=PQzRCLLHtAIQ6oXT-gM&amp;guid=ON&amp;script=0" />
	</div>
</noscript>
