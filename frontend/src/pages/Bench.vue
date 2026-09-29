<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
import BoxUnfold from '../components/BoxUnfold.vue'

const boxes = ref([])
const bid = ref(1)
const out = ref(null)
const err = ref('')
const busy = ref(false)
const tapeOn = ref(false)
const tapeMargin = ref(0)

onMounted(async () => {
  try {
    boxes.value = (await getJSON('/api/boxes')).items.filter((b) => b.data_quality === 'clean')
    if (boxes.value.length) bid.value = boxes.value[0].id
    const s = await getJSON('/api/settings')
    tapeOn.value = s.tape_enabled === 'true'
    tapeMargin.value = Number(s.tape_margin_m ?? 0)
  } catch (e) {
    err.value = String(e.message || e)
  }
})

function tapeBody() {
  const body = { tape_enabled: tapeOn.value }
  if (tapeOn.value) body.tape_margin_m = Number(tapeMargin.value) || 0
  return body
}

async function go(save) {
  err.value = ''
  busy.value = true
  try {
    out.value = save
      ? await postJSON('/api/estimate', { box_id: bid.value, save: true, ...tapeBody() })
      : await getJSON(`/api/estimate?${new URLSearchParams({ box_id: String(bid.value), ...tapeBody() })}`)
  } catch (e) {
    err.value = String(e.message || e)
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="page">
    <h1>算纸</h1>
    <p class="lede">先试算看面积与展开，确认后再写入用纸档。胶带与用纸面积分字段计算，互不并入。</p>
    <div class="row">
      <select v-model.number="bid">
        <option v-for="b in boxes" :key="b.id" :value="b.id">{{ b.name }}</option>
      </select>
      <label class="switch">
        <input v-model="tapeOn" type="checkbox" />
        封口胶带
      </label>
      <input
        v-if="tapeOn"
        v-model.number="tapeMargin"
        class="num"
        type="number"
        min="0"
        step="0.05"
      />
      <span v-if="tapeOn" class="meta">m 余量</span>
      <button :disabled="busy" @click="go(false)">试算</button>
      <button class="ribbon" :disabled="busy" @click="go(true)">写入用纸档</button>
    </div>
    <p v-if="err" class="bad">{{ err }}</p>
    <div v-if="out" class="result-board">
      <div class="figure-row">
        <div class="figure">{{ out.paper_m2 }}<span>m² 用纸面积</span></div>
        <div class="figure tape">{{ out.tape_m ?? 0 }}<span>m 封口胶带</span></div>
      </div>
      <p class="stat-line" v-if="out.ribbon">
        十字丝带约 {{ out.ribbon.ribbon_m ?? out.ribbon }} m
      </p>
      <p class="stat-line" v-if="out.tape?.enabled">
        胶带 = 2 × (长 + 宽) + 余量 {{ out.tape.tape_margin_m }} m
      </p>
      <BoxUnfold
        :l="out.box.length"
        :w="out.box.width"
        :h="out.box.height"
        :paper-m2="out.paper_m2"
      />
    </div>
  </div>
</template>
