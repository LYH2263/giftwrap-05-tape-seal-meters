<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'

const props = defineProps({ id: String })
const run = ref(null)
const err = ref('')

onMounted(async () => {
  try {
    run.value = await getJSON(`/api/runs/${props.id}`)
  } catch (e) {
    err.value = String(e.message || e)
  }
})
</script>

<template>
  <div class="page">
    <p v-if="err" class="bad">{{ err }}</p>
    <template v-else-if="run">
      <h1>{{ run.box_name }} #{{ run.id }}</h1>
      <p class="lede">以下数值取自落库记录，是该单的唯一真相，不随后续默认参数变化。</p>
      <div class="result-board">
        <div class="figure-row">
          <div class="figure">{{ run.result?.paper_m2 ?? '—' }}<span>m² 用纸面积</span></div>
          <div class="figure tape">{{ run.result?.tape_m ?? '—' }}<span>m 封口胶带</span></div>
        </div>
        <p class="stat-line" v-if="run.result?.ribbon">
          十字丝带约 {{ run.result.ribbon.ribbon_m }} m
        </p>
        <p class="stat-line">
          折边系数 ×{{ run.overlap }}<template v-if="run.result?.tape?.enabled">
            ｜胶带余量 {{ run.result.tape.tape_margin_m }} m
          </template>
        </p>
        <p class="meta">{{ run.created_at }}</p>
      </div>
      <div class="row" style="margin-top: 1.25rem">
        <router-link class="btn" to="/bench">回算纸台</router-link>
        <router-link class="btn ghost" to="/history">返回用纸档</router-link>
      </div>
    </template>
  </div>
</template>
