<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'

const s = ref({})
const err = ref('')
const saved = ref(false)
const busy = ref(false)

onMounted(load)

async function load() {
  try {
    s.value = await getJSON('/api/settings')
  } catch (e) {
    err.value = String(e.message || e)
  }
}

async function save() {
  err.value = ''
  saved.value = false
  busy.value = true
  try {
    const body = {
      tape_enabled: s.value.tape_enabled === 'true',
      tape_margin_m: Number(s.value.tape_margin_m) || 0,
    }
    s.value = await postJSON('/api/settings', body)
    saved.value = true
  } catch (e) {
    err.value = String(e.message || e)
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="page">
    <h1>设置</h1>
    <p class="lede">折边系数全局只读；封口胶带可在此登记默认开关与余量，算纸台未显式指定时按此走。已落库的单不受影响。</p>
    <p v-if="err" class="bad">{{ err }}</p>
    <ul class="item-list">
      <li>
        <span>折边系数 overlap</span>
        <span class="meta">{{ s.overlap }}</span>
      </li>
      <li>
        <span>封口胶带默认开关</span>
        <label class="switch">
          <input v-model="s.tape_enabled" type="checkbox" :true-value="'true'" :false-value="'false'" />
          {{ s.tape_enabled === 'true' ? '开' : '关' }}
        </label>
      </li>
      <li>
        <span>胶带默认余量</span>
        <span class="meta">
          <input v-model.number="s.tape_margin_m" class="num" type="number" min="0" step="0.05" /> m
        </span>
      </li>
    </ul>
    <div class="row" style="margin-top: 1.25rem">
      <button :disabled="busy" @click="save">保存设置</button>
      <span v-if="saved" class="pill">已登记</span>
    </div>
  </div>
</template>
