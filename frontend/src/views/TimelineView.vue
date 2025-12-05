<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { crmService } from "../services/api";

const timeline = ref([]);
const loading = ref(true);
const viewMode = ref("card"); 
const selectedEventTypes = ref([]);
const selectedPeriod = ref("");

const allEventTypes = [
  "company_created",
  "company_updated",
  "contact_created",
  "contact_updated",
  "deal_created",
  "deal_stage_changed",
  "task_created",
  "task_completed",
  "task_assigned",
];

const periods = [
  { label: "Today", value: "today" },
  { label: "Last Week", value: "last_week" },
  { label: "Last Month", value: "last_month" },
];

const eventColors = {
  company_created: "primary",
  company_updated: "secondary",
  contact_created: "success",
  contact_updated: "info",
  deal_created: "accent",
  deal_stage_changed: "warning",
  task_created: "orange",
  task_completed: "error",
  task_assigned: "indigo",
};

const eventIcons = {
  company_created: "mdi-office-building-plus",
  company_updated: "mdi-office-building-edit",
  contact_created: "mdi-account-plus",
  contact_updated: "mdi-account-edit",
  deal_created: "mdi-handshake",
  deal_stage_changed: "mdi-arrow-right-bold",
  task_created: "mdi-checkbox-marked-circle-outline",
  task_completed: "mdi-checkbox-marked-circle",
  task_assigned: "mdi-account-arrow-right",
};

const filteredTimeline = computed(() => {
  if (!timeline.value) return [];
  if (!selectedEventTypes.value.length) return timeline.value;
  return timeline.value.filter((event) =>
    selectedEventTypes.value.includes(event.event_type)
  );
});

const fetchTimeline = async () => {
  loading.value = true;
  try {
    const params = {};
    if (selectedPeriod.value) params.period = selectedPeriod.value;
    if (selectedEventTypes.value.length > 0) params.event_type = selectedEventTypes.value.slice();
    const res = await crmService.getTimeline(params);
    timeline.value = res || [];
  } catch (e) {
    console.error("Failed to load timeline:", e);
    timeline.value = [];
  } finally {
    loading.value = false;
  }
};

watch([selectedPeriod, selectedEventTypes], fetchTimeline);

const formatDateTime = (date) => {
  if (!date) return "";
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(date));
};

onMounted(fetchTimeline);
</script>

<template>
  <v-container fluid class="pa-6">
    <!-- Header + Clear Filters -->
    <v-row>
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center mb-4 flex-wrap gap-3">
          <div>
            <h1 class="text-h3 font-weight-bold text-navy mb-2">Activity Timeline</h1>
            <p class="text-h6 text-grey-darken-1">Track all CRM activities in real time</p>
          </div>
          <v-btn color="primary" size="large" prepend-icon="mdi-filter-remove"
            @click="selectedEventTypes = []; selectedPeriod = ''" elevation="2">
            Clear Filters
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <!-- Filters + View Toggle -->
    <v-row>
      <v-col cols="12">
        <v-card elevation="2" class="mb-5">
          <v-card-text class="pa-4 d-flex align-center gap-3 flex-wrap">
            <!-- Scrollable Chips -->
            <div style="display: flex; overflow-x: auto; white-space: nowrap; max-width: 60%;">
              <v-chip-group v-model="selectedEventTypes" multiple active-class="white--text">
                <v-chip v-for="type in allEventTypes" :key="type" :value="type" :color="eventColors[type] || 'grey'"
                  text-color="white" class="ma-1 text-capitalize" filter>
                  <v-icon size="16" class="mr-1">{{ eventIcons[type] }}</v-icon>
                  {{ type.replace(/_/g, " ") }}
                </v-chip>
              </v-chip-group>
            </div>

            <!-- Period Dropdown -->
            <v-select density="compact" label="Filter by Time Period" :items="periods" item-title="label"
              item-value="value" v-model="selectedPeriod" clearable style="max-width: 180px"></v-select>

            <!-- Spacer pushes view toggle to the right -->
            <v-spacer></v-spacer>

            <!-- View Mode Toggle -->
            <v-btn-toggle v-model="viewMode" mandatory variant="outlined" density="compact">
              <v-btn value="card" size="small"><v-icon>mdi-view-grid</v-icon></v-btn>
              <v-btn value="table" size="small"><v-icon>mdi-view-list</v-icon></v-btn>
            </v-btn-toggle>
          </v-card-text>


        </v-card>
      </v-col>
    </v-row>

    <!-- Loading -->
    <v-row v-if="loading">
      <v-col cols="12" class="text-center py-12">
        <v-progress-circular indeterminate color="primary" size="64" />
      </v-col>
    </v-row>

    <!-- Card View -->
    <v-row v-else-if="viewMode === 'card'" dense>
      <v-col v-for="event in filteredTimeline" :key="event.id" cols="12" sm="6" md="4">
        <v-card elevation="3" class="activity-card mb-5 h-100" hover>
          <v-card-text class="pa-4">
            <div class="d-flex align-center mb-3">
              <v-avatar size="46" :color="eventColors[event.event_type] || 'grey'" class="mr-3">
                <v-icon size="26">{{ eventIcons[event.event_type] }}</v-icon>
              </v-avatar>
              <div>
                <div class="font-weight-bold">{{ event.user }}</div>
                <v-chip class="text-capitalize mt-1" size="small" :color="eventColors[event.event_type]"
                  text-color="white">{{ event.event_type.replace(/_/g, ' ') }}</v-chip>
              </div>
            </div>

            <p class="text-body-2 mb-3">{{ event.description }}</p>

            <div class="text-caption text-grey-darken-1">
              <div v-if="event.company_name">Company: <strong>{{ event.company_name }}</strong></div>
              <div v-if="event.contact_name">Contact: <strong>{{ event.contact_name }}</strong></div>
              <div v-if="event.deal_name">Deal: <strong>{{ event.deal_name }}</strong></div>
              <div v-if="event.task_title">Task: <strong>{{ event.task_title }}</strong></div>
            </div>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions class="pa-3">
            <v-icon size="18" color="grey-darken-1" class="mr-1">mdi-clock-outline</v-icon>
            <span class="text-caption text-grey-darken-1">{{ formatDateTime(event.created_at) }}</span>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col v-if="filteredTimeline.length === 0" cols="12">
        <v-card elevation="2" class="pa-12 text-center">
          <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-history</v-icon>
          <h3 class="text-h5 mb-2 text-grey-darken-1">No activities found</h3>
          <p class="text-body-2 text-grey">Try adjusting your filters to see more activity.</p>
        </v-card>
      </v-col>
    </v-row>

    <!-- Table View -->
    <v-row v-else>
      <v-col cols="12">
        <v-card elevation="3">
          <v-data-table :headers="[
            { title: 'User', key: 'user' },
            { title: 'Event Type', key: 'event_type' },
            { title: 'Description', key: 'description' },
            { title: 'Company', key: 'company_name' },
            { title: 'Contact', key: 'contact_name' },
            { title: 'Deal', key: 'deal_name' },
            { title: 'Task', key: 'task_title' },
            { title: 'Date', key: 'created_at' }
          ]" :items="filteredTimeline" :loading="loading" items-per-page="10">
            <template v-slot:item.event_type="{ item }">
              <v-chip small :color="eventColors[item.event_type]" text-color="white">
                {{ item.event_type.replace(/_/g, ' ') }}
              </v-chip>
            </template>
            <template v-slot:item.created_at="{ item }">
              {{ formatDateTime(item.created_at) }}
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

  </v-container>
</template>

<style scoped>
.activity-card {
  transition: 0.3s ease;
  border-top: 4px solid transparent;
}

.activity-card:hover {
  transform: translateY(-4px);
  border-top-color: rgb(var(--v-theme-primary));
}

.activity-card .v-card-text {
  min-height: 150px;
}

.text-navy {
  color: #1a237e;
}
</style>
