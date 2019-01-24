function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function draw(resp){
    var graph = new joint.dia.Graph;

    var paper = new joint.dia.Paper({
        el: document.getElementById('canvas'),
        model: graph,
        width:800,
        height:800,
        gridSize:20,
        drawGrid: true
    });
    paper.on('cell:pointerdblclick',function(cellView,evt,x,y){
        
        var label = cellView.model.get('attrs').label.text;
        var id = [];
        for(var i =0;i<label.length;i++){
            if(label.charAt(i)<'A' || label.charAt(i)>'Z'){
                if(label.charAt(i) == ':') break;
                id.push(label.charAt(i));
            }
        }
        id = id.join('');
        //alert('cellView  '+id);
        var csrftoken = getCookie('csrftoken');
        $.ajax({

            type : "POST", // http method
            data : { 'del1' :  id,
                     'del': '1',
                        csrfmiddlewaretoken: csrftoken },
            dataType: 'json',           
            success : function(json) {
                console.log("GIRDIM");
                var arrayLength = json.connections.length;
                var str = '<ul>'
                for (var i = 0; i < arrayLength; i++)
                {
                    str += '<li>'+ json.connections[i][0] + ' - '+ json.connections[i][1]+'</li>';
                }
                str += '</ul>';
                $('#conns').replaceWith( str); 
                $('#inp').replaceWith(json.freeinpins);
                $('#out').replaceWith( json.freeoutpins);
                $('#output').replaceWith( json.output); 
                draw(json);           
                console.log("success"); // another sanity check
            }
        });

    });  

     var andFile = ['<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50">',
              
              '<path d="M30 5V45H50.47619c11.267908 0 20-9.000045 20-20s-8.732091-20-20-20H30zm2.857143 2.857143H50.47619c9.760663 0 16.666667 7.639955 16.666667 17.142857 0 9.502902-7.382195 17.142857-17.142857 17.142857H32.857143V7.857143z"/>',
            '</svg>'].join(' ');
    var orFile = ['<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50">',
          
          '<path fill-rule="evenodd" d="M24.09375 5l2 2.4375S31.75 14.437549 31.75 25s-5.65625 17.5625-5.65625 17.5625l-2 2.4375H41.25c2.408076.000001 7.689699.024514 13.625-2.40625s12.536536-7.343266 17.6875-16.875L71.25 25l1.3125-.71875C62.259387 5.21559 46.006574 5 41.25 5H24.09375zm5.875 3H41.25c4.684173 0 18.28685-.130207 27.96875 17C64.451964 33.429075 58.697469 37.68391 53.5 39.8125 48.139339 42.007924 43.658075 42.000001 41.25 42H30c1.873588-3.108434 4.75-9.04935 4.75-17 0-7.973354-2.908531-13.900185-4.78125-17z"/>',
        '</svg>'].join(' ');

    var xorFile = ['<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50">',
         
         ' <g fill-rule="evenodd">',
            '<path d="M24.25 42C22.65263 44.6444 22 45 22 45h-3.65625l2-2.4375S26 35.56245 26 25 20.34375 7.4375 20.34375 7.4375l-2-2.4375H22c.78125.9375 1.42188 1.65625 2.21875 3C26.09147 11.09981 29 17.02665 29 25c0 7.95065-2.8967 13.87942-4.75 17z"/>',
            '<path d="M24.09375 5l2 2.4375S31.75 14.43755 31.75 25s-5.65625 17.5625-5.65625 17.5625l-2 2.4375H41.25c2.40808 0 7.6897.02451 13.625-2.40625s12.53654-7.34327 17.6875-16.875L71.25 25l1.3125-.71875C62.25939 5.21559 46.00657 5 41.25 5H24.09375zm5.875 3H41.25c4.68417 0 18.28685-.1302 27.96875 17C64.45196 33.42907 58.69747 37.68391 53.5 39.8125 48.13934 42.00792 43.65808 42 41.25 42H30c1.87359-3.10843 4.75-9.04935 4.75-17 0-7.97335-2.90853-13.90019-4.78125-17z"/>',
          '</g>',
        '</svg>'].join('');

    var notFile = ['<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50">',
          
          '<path d="M28.96875 2.59375v44.8125l2.15625-1.0625 41.03125-20v-2.6875l-41.03125-20-2.15625-1.0625zm3 4.8125L68.09375 25l-36.125 17.59375V7.40625z" style="marker:none"/>',
          '<path fill="none" stroke="#000" stroke-width="3" d="M79 25a4 4 0 1 1-8 0 4 4 0 1 1 8 0z" style="marker:none"/>',
            '</svg>'].join(' ');

    var norFile = ['<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50">',
          
          '<path fill-rule="evenodd" d="M24.09375 5l2 2.4375S31.75 14.437549 31.75 25s-5.65625 17.5625-5.65625 17.5625l-2 2.4375H41.25c2.408076.000001 7.689699.024514 13.625-2.40625s12.536536-7.343266 17.6875-16.875L71.25 25l1.3125-.71875C62.259387 5.21559 46.006574 5 41.25 5H24.09375zm5.875 3H41.25c4.684173 0 18.28685-.130207 27.96875 17C64.451964 33.429075 58.697469 37.68391 53.5 39.8125 48.139339 42.007924 43.658075 42.000001 41.25 42H30c1.873588-3.108434 4.75-9.04935 4.75-17 0-7.973354-2.908531-13.900185-4.78125-17z"/>',
          '<path fill="none" stroke="#000" stroke-width="3" d="M79 25a4 4 0 1 1-8 0 4 4 0 1 1 8 0z" style="marker:none"/>',
        '</svg>'].join(' ');

    var nandFile = ['<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50">',
          
          '<path d="M30 5V45H50.47619c11.267908 0 20-9.000045 20-20s-8.732091-20-20-20H30zm2.857143 2.857143H50.47619c9.760663 0 16.666667 7.639955 16.666667 17.142857 0 9.502902-7.382195 17.142857-17.142857 17.142857H32.857143V7.857143z"/>',
          '<path fill="none" stroke="#000" stroke-width="3" d="M79 25a4 4 0 1 1-8 0 4 4 0 1 1 8 0z"/>',
        '</svg>'].join(' ');

    var equivFile = ['<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50">',
          
          '<path d="M28.96875 2.59375v44.8125l2.15625-1.0625 41.03125-20v-2.6875l-41.03125-20-2.15625-1.0625zm3 4.8125L68.09375 25l-36.125 17.59375V7.40625z" style="marker:none"/>',
            '</svg>'].join(' ');

    var switchFile = ['<svg xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" version="1.0" x="0.00000000" y="0.00000000" width="500.00000" height="500.00000" id="svg2">',
         ' <defs id="defs4"/>',
          '<g id="layer1">',
            '<rect width="300.00000" height="300.00000" x="100.00000" y="100.00000" style="opacity:1.0000000;fill:none;fill-opacity:1.0000000;fill-rule:evenodd;stroke:#000000;stroke-width:8.0000000;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4.0000000;stroke-dasharray:none;stroke-dashoffset:0.00000000;stroke-opacity:1.0000000" id="rect5719"/>',
          '</g>',
        '</svg>'].join(' ');
    
    var ledFile = ['<svg xmlns="http://www.w3.org/2000/svg" width="500" height="500">',
        '<circle cx="250" cy="250" r="210" fill="#fff" stroke="#000" stroke-width="8"/>',
        '</svg>'].join(' ');
    joint.shapes.standard.Image.define('and',{
        size:{
            width:100,
            height:100
        },
        position:{
            x:100,
            y:100
        },attrs:{
            
            image:{
                width:1024,
                height:768,
                'xlink:href':'data:image/svg+xml;utf8,'+encodeURIComponent(andFile)
            }
        }
    });

    joint.shapes.standard.Image.define('or',{
        size:{
            width:100,
            height:100
        },
        position:{
            x:100,
            y:100
        },attrs:{
            
            image:{
                width:1024,
                height:768,
                'xlink:href':'data:image/svg+xml;utf8,'+encodeURIComponent(orFile)
            }
        }
    });

    joint.shapes.standard.Image.define('xor',{
        size:{
            width:100,
            height:100
        },
        position:{
            x:100,
            y:100
        },attrs:{
            
            image:{
                width:1024,
                height:768,
                'xlink:href':'data:image/svg+xml;utf8,'+encodeURIComponent(xorFile)
            }
        }
    });

    joint.shapes.standard.Image.define('not',{
        size:{
            width:100,
            height:100
        },
        position:{
            x:100,
            y:100
        },attrs:{
            
            image:{
                width:1024,
                height:768,
                'xlink:href':'data:image/svg+xml;utf8,'+encodeURIComponent(notFile)
            }
        }
    });

    joint.shapes.standard.Image.define('nor',{
        size:{
            width:100,
            height:100
        },
        position:{
            x:100,
            y:100
        },attrs:{
            
            image:{
                width:1024,
                height:768,
                'xlink:href':'data:image/svg+xml;utf8,'+encodeURIComponent(norFile)
            }
        }
    });

    joint.shapes.standard.Image.define('nand',{
        size:{
            width:100,
            height:100
        },
        position:{
            x:100,
            y:100
        },attrs:{
            
            image:{
                width:1024,
                height:768,
                'xlink:href':'data:image/svg+xml;utf8,'+encodeURIComponent(nandFile)
            }
        }
    });

    joint.shapes.standard.Image.define('equiv',{
        size:{
            width:100,
            height:100
        },
        position:{
            x:100,
            y:100
        },attrs:{
            
            image:{
                width:1024,
                height:768,
                'xlink:href':'data:image/svg+xml;utf8,'+encodeURIComponent(equivFile)
            }
        }
    });

    joint.shapes.standard.Image.define('switch',{
        size:{
            width:100,
            height:100
        },
        position:{
            x:100,
            y:100
        },attrs:{
            
            image:{
                width:1024,
                height:768,
                'xlink:href':'data:image/svg+xml;utf8,'+encodeURIComponent(switchFile)
            }
        }
    });

    joint.shapes.standard.Image.define('led',{
        size:{
            width:100,
            height:100
        },
        position:{
            x:100,
            y:100
        },attrs:{
            
            image:{
                width:1024,
                height:768,
                'xlink:href':'data:image/svg+xml;utf8,'+encodeURIComponent(ledFile)
            }
        }
    });

    joint.shapes.standard.Image.define('in',{});

    joint.shapes.standard.Image.define('out',{});
    var comps = resp.components;
    var conns = resp.connections;
    var freein = resp.freeinpins;
    var freeout = resp.freeoutpins;
    var components = {};
    for(var i =0,c;i<comps.length;i++){
        c = comps[i];
        if(c[1] == "AND"){
            var a = new joint.shapes.and();
            a.attr({
                label:{
                    text:c[1]+c[0],
                    textVerticalAnchor:'middle',
                    textAnchor:'middle',
                    refX:'50%',
                    refY:'30%',
                    fontSize:13,
                    fill:'red'
                }
            });
            a.position(400,i*100);
            a.resize(100,50);
            a.addTo(graph);
            components[c[0]] = a;
        }else if(c[1]=="OR"){
            var a = new joint.shapes.or();
            a.attr({
                label:{
                    text:c[1]+c[0],
                    textVerticalAnchor:'middle',
                    textAnchor:'middle',
                    refX:'50%',
                    refY:'30%',
                    fontSize:13,
                    fill:'red'
                }
            });
            a.position(400,i*100);
            a.resize(100,50);
            a.addTo(graph);
            components[c[0]] = a;
        }else if(c[1]=="XOR"){
            var a = new joint.shapes.xor();
            a.attr({
                label:{
                    text:c[1]+c[0],
                    textVerticalAnchor:'middle',
                    textAnchor:'middle',
                    refX:'50%',
                    refY:'30%',
                    fontSize:13,
                    fill:'red'
                }
            });
            a.position(400,i*100);
            a.resize(100,50);
            a.addTo(graph);
            components[c[0]] = a;
        }else if(c[1]=="NOT"){
            var a = new joint.shapes.not();
            a.attr({
                label:{
                    text:c[1]+c[0],
                    textVerticalAnchor:'middle',
                    textAnchor:'middle',
                    refX:'50%',
                    refY:'30%',
                    fontSize:13,
                    fill:'red'
                }
            });
            a.position(400,i*100);
            a.resize(100,50);
            a.addTo(graph);
            components[c[0]] = a;
        }else if(c[1]=="NOR"){
            var a = new joint.shapes.nor();
            a.attr({
                label:{
                    text:c[1]+c[0],
                    textVerticalAnchor:'middle',
                    textAnchor:'middle',
                    refX:'50%',
                    refY:'30%',
                    fontSize:13,
                    fill:'red'
                }
            });
            a.position(400,i*100);
            a.resize(100,50);
            a.addTo(graph);
            components[c[0]] = a;
        }else if(c[1]=="NAND"){
            var a = new joint.shapes.nand();
            a.attr({
                label:{
                    text:c[1]+c[0],
                    textVerticalAnchor:'middle',
                    textAnchor:'middle',
                    refX:'50%',
                    refY:'30%',
                    fontSize:13,
                    fill:'red'
                }
            });
            a.position(400,i*100);
            a.resize(100,50);
            a.addTo(graph);
            components[c[0]] = a;
        }else if(c[1]=="EQUIV"){
            var a = new joint.shapes.equiv();
            a.attr({
                label:{
                    text:c[1]+c[0],
                    textVerticalAnchor:'middle',
                    textAnchor:'middle',
                    refX:'50%',
                    refY:'30%',
                    fontSize:13,
                    fill:'red'
                }
            });
            a.position(400,i*100);
            a.resize(100,50);
            a.addTo(graph);
            components[c[0]] = a;
        }else if(c[1] == "SWITCH"){
            var a = new joint.shapes.switch();
            a.attr({
                label:{
                    text:c[1]+c[0]+': '+c[3],
                    textVerticalAnchor:'middle',
                    textAnchor:'middle',
                    refX:'50%',
                    refY:'30%',
                    fontSize:13,
                    fill:'red'
                }
            });
            a.position(250,i*50);
            a.resize(100,50);
            a.addTo(graph);
            components[c[0]] = a;
        }else if(c[1]=="LED"){
            var a = new joint.shapes.led();
            a.attr({
                label:{
                    text:c[1]+c[0]+': '+c[3],
                    textVerticalAnchor:'middle',
                    textAnchor:'middle',
                    refX:'50%',
                    refY:'30%',
                    fontSize:13,
                    fill:'red'
                }
            });
            a.position(550,i*50);
            a.resize(100,50);
            a.addTo(graph);
            components[c[0]] = a;
        }
    }
    
    for(var i = 0;i<conns.length;i++){

        var dest = components[conns[i][1][0]];
        var src = components[conns[i][0][0]];
        var link = new joint.shapes.standard.Link();
        link.source(src);
        link.target(dest);
        link.addTo(graph);

        
    }
    
    for(var i =0;i<freein.length;i++){
        var dest = components[freein[i][0]];
        var src = new joint.shapes.in();
        src.attr({
            label:{
                text:"INP"+i
            }
        });
        src.position(100,i*50);
        src.addTo(graph);
        var link = new joint.shapes.standard.Link();
        link.source(src);
        link.target(dest);
        link.addTo(graph);
    }

    for(var i =0;i<freeout.length;i++){
        var dest = components[freeout[i][0]];
        var src = new joint.shapes.out();
        src.attr({
            label:{
                text:"OUT"+i
            }
        });
        src.position(700,i*100);
        src.addTo(graph);
        var link = new joint.shapes.standard.Link();
        link.source(dest);
        link.target(src);
        link.addTo(graph);
    }

}


$("#component").submit(function(e){
    e.preventDefault();
	var input_number = $('#id_input_number').val();
	var component_name = $('#id_component_name').val();
	var csrftoken = getCookie('csrftoken');
    $.ajax({
        type : "POST", // http method
        data : { 'component_name' :  component_name,
        			'input_number' : input_number ,
                    'del': '0',
        			csrfmiddlewaretoken: csrftoken },
        dataType: 'json',			
        success : function(json) {
            // remove the value from the input
             // log the returned json to the console
            var arrayLength = json.connections.length;
            var str =  '<div id="conns">'; 
            str += '<ul>'
            for (var i = 0; i < arrayLength; i++)
            {
                str += '<li>'+ json.connections[i][0] + ' - '+ json.connections[i][1]+'</li>';
            }
            str += '</ul>';
            str += '</div>';
            var arrayLen = json.output.length;
            var str1 = '<div id="x">'; 
            str1 += '<ul>';
            for (var i = 0; i < arrayLen; i++)
            {
                str1 += '<li>'+ json.output[i] + '</li>';
            }
            str1 += '</ul>';
            str1 += '</div>'; 

            $('#conns').replaceWith( str); 
            $('#inp').replaceWith(json.freeinpins);
            $('#out').replaceWith( json.freeoutpins);
            $('#x').replaceWith( str1);
            console.log(json.output);

            draw(json);            
            console.log("success"); // another sanity check
        }
    });
})

$("#connect").submit(function(e){
    e.preventDefault();
	var component1 = $('#id_component1').val();
	var connection1 = $('#id_connection1').val();
	var component2 = $('#id_component2').val();
	var connection2 = $('#id_connection2').val();	
	var csrftoken = getCookie('csrftoken');
    $.ajax({
        type : "POST", // http method
        data : { 'component1' :  component1,
        			'connection1' : connection1 ,
        			'component2' : component2,
        			'connection2' : connection2,
                    'del': '0',
        			csrfmiddlewaretoken: csrftoken },
        dataType: 'json',			
        success : function(json) {
            // remove the value from the input


            var arrayLength = json.connections.length;
            var str =  '<div id="conns">'; 
            str += '<ul>'
            for (var i = 0; i < arrayLength; i++)
            {
                str += '<li>'+ json.connections[i][0] + ' - '+ json.connections[i][1]+'</li>';
            }
            str += '</ul>';
            str += '</div>';
            var arrayLen = json.output.length;
            var str1 = '<div id="x">'; 
            str1 += '<ul>';
            for (var i = 0; i < arrayLen; i++)
            {
                str1 += '<li>'+ json.output[i] + '</li>';
            }
            str1 += '</ul>';
            str1 += '</div>'; 

            $('#conns').replaceWith( str); 
            $('#inp').replaceWith(json.freeinpins);
            $('#out').replaceWith( json.freeoutpins);
            $('#x').replaceWith( str1);
            console.log(json.output);

            draw(json);            
            console.log("success"); // another sanity check
        }
    });
})

$("#disconnect").submit(function(e){
    e.preventDefault();
	var component1 = $('#id_comp1').val();
	var connection1 = $('#id_conn1').val();
	var component2 = $('#id_comp2').val();
	var connection2 = $('#id_conn2').val();	
	var csrftoken = getCookie('csrftoken');
    $.ajax({
        type : "POST", // http method
        data : { 'comp1' :  component1,
        			'conn1' : connection1 ,
        			'comp2' : component2,
        			'conn2' : connection2,
                    'del': '0',
        			csrfmiddlewaretoken: csrftoken },
        dataType: 'json',			
        success : function(json) {
            var arrayLength = json.connections.length;
            var str =  '<div id="conns">'; 
            str += '<ul>'
            for (var i = 0; i < arrayLength; i++)
            {
                str += '<li>'+ json.connections[i][0] + ' - '+ json.connections[i][1]+'</li>';
            }
            str += '</ul>';
            str += '</div>';
            var arrayLen = json.output.length;
            var str1 = '<div id="x">'; 
            str1 += '<ul>';
            for (var i = 0; i < arrayLen; i++)
            {
                str1 += '<li>'+ json.output[i] + '</li>';
            }
            str1 += '</ul>';
            str1 += '</div>'; 

            $('#conns').replaceWith( str); 
            $('#inp').replaceWith(json.freeinpins);
            $('#out').replaceWith( json.freeoutpins);
            $('#x').replaceWith( str1);
            console.log(json.output);

            draw(json);            
            console.log("success"); // another sanity check
        }
    });
})

$("#switchSet").submit(function(e){
    e.preventDefault();
	var component1 = $('#id_switchNo').val();
	var connection1 = $('#id_setNo').val();
	var csrftoken = getCookie('csrftoken');
    $.ajax({
        type : "POST", // http method
        data : { 'switchNo' :  component1,
        			'setNo' : connection1 ,
                    'del': '0',
        			csrfmiddlewaretoken: csrftoken },
        dataType: 'json',			
        success : function(json) {
            var arrayLength = json.connections.length;
            var str =  '<div id="conns">'; 
            str += '<ul>'
            for (var i = 0; i < arrayLength; i++)
            {
                str += '<li>'+ json.connections[i][0] + ' - '+ json.connections[i][1]+'</li>';
            }
            str += '</ul>';
            str += '</div>';
            var arrayLen = json.output.length;
            var str1 = '<div id="x">'; 
            str1 += '<ul>';
            for (var i = 0; i < arrayLen; i++)
            {
                str1 += '<li>'+ json.output[i] + '</li>';
            }
            str1 += '</ul>';
            str1 += '</div>'; 

            $('#conns').replaceWith( str); 
            $('#inp').replaceWith(json.freeinpins);
            $('#out').replaceWith( json.freeoutpins);
            $('#x').replaceWith( str1);
            console.log(json.output);

            draw(json);            
            console.log("success"); // another sanity check
        }
    });
})

$("#delComponent").submit(function(e){
    e.preventDefault();
	var component1 = $('#id_del1').val();
	var csrftoken = getCookie('csrftoken');
    $.ajax({
        type : "POST", // http method
        data : { 'del1' :  component1,
        'del': '0',
        			csrfmiddlewaretoken: csrftoken },
        dataType: 'json',			
        success : function(json) {
            var arrayLength = json.connections.length;
            var str =  '<div id="conns">'; 
            str += '<ul>'
            for (var i = 0; i < arrayLength; i++)
            {
                str += '<li>'+ json.connections[i][0] + ' - '+ json.connections[i][1]+'</li>';
            }
            str += '</ul>';
            str += '</div>';
            var arrayLen = json.output.length;
            var str1 = '<div id="x">'; 
            str1 += '<ul>';
            for (var i = 0; i < arrayLen; i++)
            {
                str1 += '<li>'+ json.output[i] + '</li>';
            }
            str1 += '</ul>';
            str1 += '</div>'; 

            $('#conns').replaceWith( str); 
            $('#inp').replaceWith(json.freeinpins);
            $('#out').replaceWith( json.freeoutpins);
            $('#x').replaceWith( str1);
            console.log(json.output);
            draw(json);            
            console.log("success"); // another sanity check
        }
    });
})

$("#set").submit(function(e){
    e.preventDefault();
	var component1 = $('#id_inputs').val();
	var csrftoken = getCookie('csrftoken');
    $.ajax({
        type : "POST", // http method
        data : { 'inputs' :  component1,
        'del': '0',
        			csrfmiddlewaretoken: csrftoken },
        dataType: 'json',			
        success : function(json) {
            var arrayLength = json.connections.length;
            var str =  '<div id="conns">'; 
            str += '<ul>'
            for (var i = 0; i < arrayLength; i++)
            {
                str += '<li>'+ json.connections[i][0] + ' - '+ json.connections[i][1]+'</li>';
            }
            str += '</ul>';
            str += '</div>';
            var arrayLen = json.output.length;
            var str1 = '<div id="x">'; 
            str1 += '<ul>';
            for (var i = 0; i < arrayLen; i++)
            {
                str1 += '<li>'+ json.output[i] + '</li>';
            }
            str1 += '</ul>';
            str1 += '</div>'; 

            $('#conns').replaceWith( str); 
            $('#inp').replaceWith(json.freeinpins);
            $('#out').replaceWith( json.freeoutpins);
            $('#x').replaceWith( str1);
            console.log(json.output);
            console.log(str1);

            draw(json);            
            console.log("success"); // another sanity check
        }
    });
})

$("#save").submit(function(e){
    e.preventDefault();
	var csrftoken = getCookie('csrftoken');
    $.ajax({
        type : "POST", // http method
        data : { 
                'del': '0',
        			csrfmiddlewaretoken: csrftoken },
        dataType: 'json',			
        success : function(json) {
            var arrayLength = json.connections.length;
            var str =  '<div id="conns">'; 
            str += '<ul>'
            for (var i = 0; i < arrayLength; i++)
            {
                str += '<li>'+ json.connections[i][0] + ' - '+ json.connections[i][1]+'</li>';
            }
            str += '</ul>';
            str += '</div>';
            var arrayLen = json.output.length;
            var str1 = '<div id="x">'; 
            str1 += '<ul>';
            for (var i = 0; i < arrayLen; i++)
            {
                str1 += '<li>'+ json.output[i] + '</li>';
            }
            str1 += '</ul>';
            str1 += '</div>'; 
            $('#conns').replaceWith( str); 
            $('#inp').replaceWith(json.freeinpins);
            $('#out').replaceWith( json.freeoutpins);
            $('#x').replaceWith( str1);
            console.log(json.output);
            draw(json);            
            console.log("success"); // another sanity check
        }
    });
})

$("#show").submit(function(e){
    e.preventDefault();
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        type : "POST", // http method
        data : { 'del': '2',
                    csrfmiddlewaretoken: csrftoken },
        dataType: 'json',           
        success : function(json) {
            var arrayLength = json.connections.length;
            var str =  '<div id="conns">'; 
            str += '<ul>'
            for (var i = 0; i < arrayLength; i++)
            {
                str += '<li>'+ json.connections[i][0] + ' - '+ json.connections[i][1]+'</li>';
            }
            str += '</ul>';
            str += '</div>';
            var arrayLen = json.output.length;
            var str1 = '<div id="x">'; 
            str1 += '<ul>';
            for (var i = 0; i < arrayLen; i++)
            {
                str1 += '<li>'+ json.output[i] + '</li>';
            }
            str1 += '</ul>';
            str1 += '</div>'; 

            $('#conns').replaceWith( str); 
            $('#inp').replaceWith(json.freeinpins);
            $('#out').replaceWith( json.freeoutpins);
            $('#x').replaceWith( str1);
            console.log(json.output)
            draw(json);            
            console.log("success"); // another sanity check
        }
    });
})





