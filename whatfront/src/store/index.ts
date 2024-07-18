// store/index.ts
import { defineStore} from 'pinia'
import { h, ref, type Component } from 'vue'

export const useUserStore = defineStore('user', () => {
  const username = ref('')

  const setUsername = (name: string) => {
    username.value = name
  }

  return {
    username,
    setUsername
  }
})

export const useEditorStore = defineStore('editor', () => {
  const headings = ref()
  const activeHeading = ref()
  const editorInstance = ref()
  const setHeadings = (data) => {
    headings.value = data
  }
  const setActiveHeading = (data) => {
    activeHeading.value = data
  }
  const setEditorInstance = (data) => {
    console.log(editorInstance.value)

    editorInstance.value = data
  }
  return {
    headings,
    setHeadings,
    activeHeading,
    setActiveHeading,
    editorInstance,
    setEditorInstance
  }
})
