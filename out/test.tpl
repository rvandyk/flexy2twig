{%  for index,item in menu_front.getItems()  %}
<li  id="ID{{ item.id }}">
  
{% if category %} 
{% if category.root %} 
{% if Math.equal(category.root.id,item.idcategory) %}
  <a href="
{{ item.uri }}" title="
{{ item.name|raw }}" class="selected" data-color="
{{ item.classes }}" data-id="
{{ item.id }}">
                                        {% else  %}
                                                <a href="
{{ item.uri }}" title="
{{ item.name|raw }}" data-color="
{{ item.classes }}" data-id="
{{ item.id }}">
                                        {% endif  %}
                                {% else  %}
                                        {% if Math.equal(category.id,item.idcategory) %}
                                                <a href="
{{ item.uri }}" title="
{{ item.name|raw }}" class="selected" data-color="
{{ item.classes }}" data-id="
{{ item.id }}">
                                        {% else  %}
                                                <a href="
{{ item.uri }}" title="
{{ item.name|raw }}" data-color="
{{ item.classes }}" data-id="
{{ item.id }}">
                                        {% endif  %}
                                {% endif  %}
                        {% else  %}
                                <a href="
{{ item.uri }}" title="
{{ item.name|raw }}" data-color="
{{ item.classes }}" data-id="
{{ item.id }}">
                        {% endif  %}
                        {{ item.name|raw }}</a>
</li>
{%  endfor  %}
