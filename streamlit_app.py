import streamlit as st

from streamlit_ace import st_ace

from barfi import st_barfi, barfi_schemas, Block

st.set_page_config(layout='wide')
st.title('WebChucK')

col1, col2 = st.columns(2)

ckdoc = {
    'osc': [
        ['SinOsc', ['freq'], ['out']],
        ['PulseOsc', ['freq'], ['out']],
        ['SqrOsc', ['freq'], ['out']],
        ['TriOsc', ['freq'], ['out']],
        ['SawOsc', ['freq'], ['out']],
    ],
    'effect': [
        ['Gain', ['in', 'gain'], ['out']],
        ['JCRev', ['in', 'mix'], ['out']],
    ],
    'system': [
        ['adc', [], ['out']],
        ['dac', ['in'], []],
        ['blackhole', ['in'], []],
    ]
}
base_blocks = {}
for k, v in ckdoc.items():
    base_blocks[k] = []
    for b in v:
        tmp = Block(name=b[0])
        for name in b[1]:
            tmp.add_input(name=name)
        for name in b[2]:
            tmp.add_output(name=name)
        def tmp_func(self):
            output = ''
            if 'in' in b[1]:
                output = self.get_interface(name='in') + ' => '
            output += f'{b[0]} {self.name}'
            if 'out' in b[2]:
                self.set_interface(name='out', value=output)
        tmp.add_compute(tmp_func)
        base_blocks[k].append(tmp)
with col1:
    barfi_result = st_barfi(base_blocks=base_blocks, compute_engine=True, load_schema='default')
    if barfi_result:
        print(barfi_result)

with col2:
    content = st_ace(value='// patch\nSinOsc sinosc_1 => Gain gain_1 => dac;\n\nwhile (true)\n{\n\t// update parameters here\n\t100::ms => now;\n}', height=1000, language='java', theme='gruvbox')