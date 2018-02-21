<%inherit file="/default.html"/>\
<%namespace name="Base" file="/base.mako"/>
<%def name="includes()">
</%def>



<div class="content iiiformatics">
    <div class="content_left_column">
        ${Base.content_menu_mcri(url.environ['pylons.routes_dict']['action'])}
    </div>
    <div class="content_right_column ">
        <div class="box display">
            <div id="introduction" class="content_box">
                <a id="introduction"></a>
                <div class="header_1">
                     Stem Cells at the Murdoch Children's Research Institute
                </div>
                <div class="text">
                <p>
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras congue lectus nec justo commodo volutpat. Integer at lorem malesuada nisl pretium tempor nec a nisi. Etiam fermentum suscipit magna. Sed auctor felis lorem, nec feugiat ex congue nec. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Phasellus eget luctus nulla. Etiam a auctor lacus. Aliquam libero nunc, dictum et condimentum id, tincidunt iaculis velit. Phasellus eu egestas metus, quis volutpat tortor. Sed vehicula nec enim vel viverra. Proin euismod facilisis enim, sit amet rutrum est molestie sed.
                <ul>
                    <li>
                        <a target="_blank" href="https://www.mcri.edu.au/research/themes/cell-biology/blood-cell-development-disease">
                            Blood Cell Development and Disease Laboratory
                        </a>
                    </li>
                    <li>
                        <a target="_blank" href="https://www.mcri.edu.au/research/themes/cell-biology/stem-cell-technology">
Stem Cell Technology Group 
                        </a>
                    </li>
                    <li>
                        <a  target="_blank" href="https://www.mcri.edu.au/research/themes/cell-biology/cardiac-development">
Cardiac Development Laboratory
                        </a>
                    </li>
                </ul>
                </p>
                <p>
In sit amet magna ultricies, accumsan purus ut, rhoncus erat. Morbi ligula libero, euismod quis venenatis at, venenatis eu turpis. Sed tempus, ex sit amet viverra sagittis, enim ante sodales turpis, vel pretium ex sem sit amet purus. Fusce tincidunt scelerisque lectus, a sagittis lorem efficitur ut. Integer eleifend mi in venenatis tincidunt. Maecenas elementum, purus sed sagittis tempor, ipsum mauris rutrum tellus, ac eleifend felis sem eu sem. Nullam ac velit sit amet ex maximus ullamcorper. Quisque vulputate varius vestibulum. Cras mattis efficitur tempus.
                </p>
                <p>
                <ul>
                    <li>
                        <a target = "_blank" href="${h.url('/datasets/search?filter=mcri')}">View Datasets associated with the Murdoch Children's Research Institute</a>
                    </li>
                </ul>
                </p>
                </div>        
            </div>        
        </div>
    </div>
</div>

