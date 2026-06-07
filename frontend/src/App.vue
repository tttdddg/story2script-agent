<template>
  <router-view />
</template>

<script setup lang="ts">
</script>

<style>
/* ═══════════════════════════════════════════════
   Story2Script — Neumorphic Design System
   ═══════════════════════════════════════════════ */

:root {
  /* Background */
  --neu-bg: #e0e5ec;
  --neu-bg-light: #e8ecf1;
  --neu-bg-lighter: #eef1f5;
  --neu-bg-dark: #d6dbe3;

  /* Shadows */
  --neu-shadow-out: 6px 6px 14px #b8bcc2, -6px -6px 14px #ffffff;
  --neu-shadow-in: inset 6px 6px 14px #b8bcc2, inset -6px -6px 14px #ffffff;
  --neu-shadow-sm-out: 3px 3px 7px #b8bcc2, -3px -3px 7px #ffffff;
  --neu-shadow-sm-in: inset 3px 3px 7px #b8bcc2, inset -3px -3px 7px #ffffff;
  --neu-shadow-hover: 4px 4px 10px #b8bcc2, -4px -4px 10px #ffffff;

  /* Radius */
  --neu-radius: 16px;
  --neu-radius-lg: 20px;
  --neu-radius-sm: 10px;

  /* Text */
  --text-primary: #2d3436;
  --text-secondary: #636e72;
  --text-hint: #a0aab4;

  /* Accent colors — soft muted tones */
  --accent-blue: #6c8ebf;
  --accent-blue-light: #e8eff6;
  --accent-green: #7dbf8c;
  --accent-green-light: #eaf5ed;
  --accent-purple: #9b8ec4;
  --accent-purple-light: #f0edf7;
  --accent-orange: #d4a574;
  --accent-orange-light: #faf3eb;
  --accent-red: #d48484;
  --accent-red-light: #faf0f0;
}

/* ── Base ── */
body {
  margin: 0;
  padding: 0;
  background: var(--neu-bg);
  font-family: 'Inter', 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif;
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* ── Element Plus Global Overrides ── */

/* Cards */
.el-card {
  background: var(--neu-bg-light) !important;
  border: none !important;
  border-radius: var(--neu-radius) !important;
  box-shadow: var(--neu-shadow-out) !important;
}
.el-card__header {
  border-bottom: 1px solid rgba(0,0,0,0.05) !important;
  padding: 14px 20px !important;
  font-weight: 600;
  color: var(--text-primary);
}
.el-card__body {
  padding: 16px 20px !important;
}

/* Buttons — base override */
.el-button {
  border-radius: var(--neu-radius-sm) !important;
  font-weight: 500 !important;
  border: none !important;
  box-shadow: var(--neu-shadow-sm-out) !important;
  transition: all 0.2s ease !important;
}
.el-button:hover {
  box-shadow: var(--neu-shadow-hover) !important;
  transform: translateY(-1px);
}
.el-button:active {
  box-shadow: var(--neu-shadow-sm-in) !important;
  transform: translateY(0);
}

/* Primary button — soft blue */
.el-button--primary {
  background: var(--accent-blue) !important;
  color: #fff !important;
}
.el-button--primary:hover {
  background: #7d9dc9 !important;
}

/* Success button — soft green */
.el-button--success {
  background: var(--accent-green) !important;
  color: #fff !important;
}
.el-button--success:hover {
  background: #8cc999 !important;
}

/* Warning button — soft orange */
.el-button--warning {
  background: var(--accent-orange) !important;
  color: #fff !important;
}

/* Info button — soft purple */
.el-button--info {
  background: var(--accent-purple) !important;
  color: #fff !important;
}

/* Default / plain buttons */
.el-button--default,
.el-button.is-plain {
  background: var(--neu-bg-light) !important;
  color: var(--text-primary) !important;
  border: none !important;
}
.el-button--default:hover,
.el-button.is-plain:hover {
  color: var(--accent-blue) !important;
}

/* Link button */
.el-button.is-link {
  box-shadow: none !important;
  background: transparent !important;
}

/* Input / Textarea */
.el-input__wrapper,
.el-textarea__inner {
  background: var(--neu-bg) !important;
  border: none !important;
  border-radius: var(--neu-radius-sm) !important;
  box-shadow: var(--neu-shadow-sm-in) !important;
  color: var(--text-primary) !important;
  font-family: inherit !important;
}
.el-input__wrapper:hover,
.el-textarea__inner:hover {
  box-shadow: var(--neu-shadow-sm-in) !important;
}
.el-input__wrapper.is-focus,
.el-textarea__inner:focus {
  box-shadow: var(--neu-shadow-sm-in), 0 0 0 2px var(--accent-blue-light) !important;
}

/* Tags */
.el-tag {
  border: none !important;
  border-radius: 6px !important;
  font-weight: 500 !important;
}
.el-tag--default {
  background: var(--neu-bg) !important;
  color: var(--text-secondary) !important;
}
.el-tag--success {
  background: var(--accent-green-light) !important;
  color: #5a9a6a !important;
}
.el-tag--danger {
  background: var(--accent-red-light) !important;
  color: #b87070 !important;
}
.el-tag--warning {
  background: var(--accent-orange-light) !important;
  color: #b89060 !important;
}
.el-tag--primary {
  background: var(--accent-blue-light) !important;
  color: #5a7ea9 !important;
}

/* Steps */
.el-step__title {
  font-size: 0.85rem !important;
  font-weight: 500 !important;
  color: var(--text-secondary) !important;
}
.el-step__title.is-process {
  color: var(--accent-blue) !important;
  font-weight: 600 !important;
}
.el-step__title.is-success {
  color: var(--accent-green) !important;
}
.el-step__description {
  font-size: 0.75rem !important;
  color: var(--text-hint) !important;
}

/* Tabs */
.el-tabs__header {
  margin-bottom: 12px !important;
}
.el-tabs__item {
  color: var(--text-secondary) !important;
  font-weight: 500 !important;
  padding: 0 16px !important;
  height: 40px !important;
  line-height: 40px !important;
}
.el-tabs__item.is-active {
  color: var(--accent-blue) !important;
}
.el-tabs__active-bar {
  background-color: var(--accent-blue) !important;
}

/* Divider */
.el-divider__text {
  background: var(--neu-bg-light) !important;
  color: var(--text-hint) !important;
  font-weight: 500 !important;
}

/* Alert */
.el-alert {
  border-radius: var(--neu-radius-sm) !important;
  border: none !important;
}

/* Table */
.el-table {
  background: transparent !important;
  --el-table-border-color: transparent !important;
}
.el-table th.el-table__cell {
  background: var(--neu-bg) !important;
  color: var(--text-secondary) !important;
  font-weight: 600 !important;
  border-bottom: 2px solid rgba(0,0,0,0.05) !important;
}
.el-table td.el-table__cell {
  border-bottom: 1px solid rgba(0,0,0,0.03) !important;
}

/* Dialog */
.el-dialog {
  border-radius: var(--neu-radius-lg) !important;
  background: var(--neu-bg-light) !important;
  box-shadow: var(--neu-shadow-out), 0 20px 60px rgba(0,0,0,0.15) !important;
}

/* Popover */
.el-popover {
  border-radius: var(--neu-radius) !important;
  background: var(--neu-bg-light) !important;
  box-shadow: var(--neu-shadow-out) !important;
  border: none !important;
}

/* Result */
.el-result__title {
  color: var(--text-primary) !important;
}
.el-result__subtitle {
  color: var(--text-secondary) !important;
}

/* Timeline */
.el-timeline-item__node {
  background: var(--neu-bg-light) !important;
  box-shadow: var(--neu-shadow-sm-out) !important;
}

/* Collapse */
.el-collapse {
  border: none !important;
}
.el-collapse-item__header {
  background: transparent !important;
  border: none !important;
}
.el-collapse-item__wrap {
  border: none !important;
  background: transparent !important;
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background: var(--neu-bg);
  border-radius: 3px;
}
::-webkit-scrollbar-thumb {
  background: #c0c5cc;
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: #a8aeb5;
}
</style>
