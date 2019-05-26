//Dont change it
requirejs(['ext_editor_io', 'jquery_190', 'raphael_210'],
    function (extIO, $) {
        function visibilitiesCanvas(dom, input, data) {

            if (! data || ! data.ext) {
                return
            }

            $(dom.parentNode).find(".answer").remove()
            
            const result = data.ext.result
            const output = data.out
            const result_addon_00 = data.ext.result_addon[0]
            const result_addon_01 = data.ext.result_addon[1]
            const result_addon_02 = data.ext.result_addon[2]
            const result_addon_03 = data.ext.result_addon[3]

            /*----------------------------------------------*
             *
             * input
             *
             *----------------------------------------------*/
            const attr = {
                grid: {
                    empty: {
                        'stroke': '#2080B8',
                    },
                    block: {
                        'stroke': '#2080B8',
                        'fill': '#8FC7ED',
                    },
                    error: {
                        'stroke': '#2080B8',
                        'fill': '#faba00',
                    },
                },
                number: {
                    'font-family': 'san-serif',
                    'font-weight': 'bold',
                    'fill': '#163e69',
                },
                ray: {
                    'stroke': '#faba00',
                },
            }

            /*----------------------------------------------*
             *
             * paper
             *
             *----------------------------------------------*/
            const width = input[0].length
            const height = input.length

            let max_width = 350
            const os = 10
            const SIZE = (max_width - os*2) / Math.max(4, width)
            max_width = Math.min(350, SIZE*width+os*2)
            const paper = Raphael(dom, max_width, SIZE*height+os*2, 0, 0)

            /*----------------------------------------------*
             *
             * black dictionary
             *
             *----------------------------------------------*/
            const blacks = {}
            if (result_addon_01 === 'Valid') {
                output.forEach(co=>{
                    const [y, x] = co
                    blacks[y*100+x] = 1
                })
            }

            /*----------------------------------------------*
             *
             * error visibility
             *
             *----------------------------------------------*/
            if (result_addon_02 === 3) {
                const [t, b, l, r] = result_addon_03
                const [top, x] = t
                const [y, left] = l
                const bottom = b[0]
                const right = r[1]

                const v_ray = paper.path(['M', x*SIZE+os+SIZE/2, 
                  (top+1)*SIZE+os, 'L', x*SIZE+os+SIZE/2, 
                  (bottom)*SIZE+os].join(' '))
                v_ray.attr({'stroke-width': 38/(width/7)}).attr(attr.ray)

                const h_ray = paper.path(['M', (left+1)*SIZE+os, 
                  y*SIZE+os+SIZE/2,
                  'L', (right)*SIZE+os, y*SIZE+os+SIZE/2].join(' '))
                h_ray.attr({'stroke-width': 38/(width/7)}).attr(attr.ray)
            }

            /*----------------------------------------------*
             *
             * error separated
             *
             *----------------------------------------------*/
            const boundary_blocks = {}
            if (result_addon_02 === 2) {
                output.forEach(([r, c])=>{
                    const adjs = [[r-1, c], [r+1, c], [r, c-1], [r, c+1]]
                    const area_sets = new Set(
                        adjs.filter(
                            ([r, c])=>r < height && r >= 0 && c < width &&
                            c >= 0).map(([r, c])=>result_addon_03[r][c]))
                    if (area_sets.size > 1) {
                        boundary_blocks[r*100+c] = 1
                    }
                })
            }

            /*----------------------------------------------*
             *
             * draw grid
             *
             *----------------------------------------------*/
            for (let r = 0; r < height; r += 1) {
                paper.rect(os, SIZE*r+os, SIZE*width, SIZE).attr(
                    attr.grid.empty)
                for (let c = 0; c < width; c += 1) {
                    // grid
                    if (r === 0) {
                        paper.rect(
                            SIZE*c+os, os, SIZE, SIZE*height).attr(
                            attr.grid.empty)
                    }

                    // error 0, 1
                    if ((result_addon_02 === 0 || result_addon_02 === 1)
                        && result_addon_03[0][0] === r
                        && result_addon_03[0][1] === c) { 

                        paper.rect(SIZE*c+os, SIZE*r+os, SIZE, SIZE).attr(
                            attr.grid.error)

                    // error 2
                    } else if (result_addon_02 === 2 &&
                        boundary_blocks[r*100+c]) {

                        paper.rect(SIZE*c+os, SIZE*r+os, SIZE, SIZE).attr(
                            attr.grid.error)

                    // normal
                    } else if (blacks[r*100+c] === 1) {
                        paper.rect(SIZE*c+os, SIZE*r+os, SIZE, SIZE).attr(
                            attr.grid.block)
                    }

                    // number
                    if (input[r][c] > 0) {
                        const num = paper.text(SIZE*c+os+SIZE*.5, 
                            SIZE*r+os+SIZE*.5, input[r][c])
                        num.attr({'font-size': 200/width}).attr(
                            attr.number)
                    }
                }
            }
            if (! result) {
                $(dom).addClass('output').prepend(
                    '<div>' + result_addon_00 + '</div>')
            }
        }

        var $tryit;

        var io = new extIO({
            multipleArguments: false,
            functions: {
                python: 'visibilities',
                //js: 'visibilities'
            },
            animation: function($expl, data){
                visibilitiesCanvas(
                    $expl[0],
                    data.in,
                    data,
                );
            }
        });
        io.start();
    }
);
