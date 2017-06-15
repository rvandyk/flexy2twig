<li flexy:foreach="menu_front.getItems(),index,item" id="ID{item.id}">
  {if:category} {if:category.root} {if:Math.equal(category.root.id,item.idcategory)}
  <a href="{item.uri}" title="{item.name:h}" class="selected" data-color="{item.classes}" data-id="{item.id}">
                                        {else:}
                                                <a href="{item.uri}" title="{item.name:h}" data-color="{item.classes}" data-id="{item.id}">
                                        {end:}
                                {else:}
                                        {if:Math.equal(category.id,item.idcategory)}
                                                <a href="{item.uri}" title="{item.name:h}" class="selected" data-color="{item.classes}" data-id="{item.id}">
                                        {else:}
                                                <a href="{item.uri}" title="{item.name:h}" data-color="{item.classes}" data-id="{item.id}">
                                        {end:}
                                {end:}
                        {else:}
                                <a href="{item.uri}" title="{item.name:h}" data-color="{item.classes}" data-id="{item.id}">
                        {end:}
                        {item.name:h}</a>
</li>
