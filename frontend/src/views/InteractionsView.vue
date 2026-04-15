<script setup>
import { ref, onMounted, computed } from 'vue'
import { crmService } from '../services/api'

const interactions = ref([])
const contacts = ref([])
const companies = ref([])
const deals = ref([])
const loading = ref(true)
const dialog = ref(false)
const viewMode = ref('card')
const search = ref('')
const error = ref('')
const editedIndex = ref(-1)

const selectedType = ref(null)
const selectedContact = ref(null)
const selectedCompany = ref(null)
const selectedFollowUpStatus = ref(null)

const editedItem = ref({
  contact: null,
  company: null,
  deal: null,
  interaction_type: 'call',
  subject: '',
  notes: '',
  interaction_date: '',
  follow_up_date: '',
})

const defaultItem = {
  contact: null,
  company: null,
  deal: null,
  interaction_type: 'call',
  subject: '',
  notes: '',
  interaction_date: '',
  follow_up_date: '',
}

const interactionTypeOptions = [
  { title: 'Call', value: 'call' },
  { title: 'Email', value: 'email' },
  { title: 'Meeting', value: 'meeting' },
  { title: 'Note', value: 'note' },
]

const followUpStatusOptions = [
  { title: 'Overdue Follow-ups', value: 'overdue' },
  { title: 'Upcoming Follow-ups', value: 'upcoming' },
]

const headers = [
  { title: 'Subject', key: 'subject', sortable: true },
  { title: 'Type', key: 'interaction_type', sortable: true },
  { title: 'Contact', key: 'contact_name', sortable: true },
  { title: 'Company', key: 'company_name', sortable: true },
  { title: 'Deal', key: 'deal_title', sortable: true },
  { title: 'Interaction Date', key: 'interaction_date', sortable: true },
  { title: 'Follow-up', key: 'follow_up_date', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' },
]

const activeFiltersCount = computed(() => {
  let count = 0
  if (selectedType.value) count++
  if (selectedContact.value) count++
  if (selectedCompany.value) count++
  if (selectedFollowUpStatus.value) count++
  return count
})

const filteredInteractions = computed(() => {
  if (!search.value) return interactions.value
  const s = search.value.toLowerCase()

  return interactions.value.filter(interaction =>
    (interaction.subject && interaction.subject.toLowerCase().includes(s)) ||
    (interaction.interaction_type && interaction.interaction_type.toLowerCase().includes(s)) ||
    (interaction.contact_name && interaction.contact_name.toLowerCase().includes(s)) ||
    (interaction.company_name && interaction.company_name.toLowerCase().includes(s)) ||
    (interaction.deal_title && interaction.deal_title.toLowerCase().includes(s)) ||
    (interaction.notes && interaction.notes.toLowerCase().includes(s))
  )
})

onMounted(async () => {
  await Promise.all([
    loadContacts(),
    loadCompanies(),
    loadDeals(),
  ])
  await loadInteractions()
})

const loadInteractions = async () => {
  loading.value = true
  error.value = ''
  try {
    const params = {}

    if (selectedType.value) params.interaction_type = selectedType.value
    if (selectedContact.value) params.contact = selectedContact.value
    if (selectedCompany.value) params.company = selectedCompany.value
    if (selectedFollowUpStatus.value) params.follow_up_status = selectedFollowUpStatus.value

    interactions.value = await crmService.getInteractions(params)
  } catch (err) {
    console.error('Failed to load interactions:', err)
    error.value = 'Failed to load interactions.'
  } finally {
    loading.value = false
  }
}

const loadContacts = async () => {
  try {
    contacts.value = await crmService.getContacts()
  } catch (err) {
    console.error('Failed to load contacts:', err)
  }
}

const loadCompanies = async () => {
  try {
    companies.value = await crmService.getCompanies()
  } catch (err) {
    console.error('Failed to load companies:', err)
  }
}

const loadDeals = async () => {
  try {
    deals.value = await crmService.getDeals()
  } catch (err) {
    console.error('Failed to load deals:', err)
  }
}

const applyFilters = async () => {
  await loadInteractions()
}

const clearFilters = async () => {
  selectedType.value = null
  selectedContact.value = null
  selectedCompany.value = null
  selectedFollowUpStatus.value = null
  await loadInteractions()
}

const getTypeColor = (type) => {
  const colors = {
    call: 'blue',
    email: 'green',
    meeting: 'purple',
    note: 'orange',
  }
  return colors[type] || 'grey'
}

const getTypeIcon = (type) => {
  const icons = {
    call: 'mdi-phone',
    email: 'mdi-email',
    meeting: 'mdi-account-group',
    note: 'mdi-note-text',
  }
  return icons[type] || 'mdi-message'
}

const getInteractionColor = (index) => {
  const colors = ['primary', 'secondary', 'success', 'info', 'warning', 'purple', 'pink', 'indigo', 'teal', 'orange']
  return colors[index % colors.length]
}

const formatDateTime = (dateValue) => {
  if (!dateValue) return 'No date'
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  }).format(new Date(dateValue))
}

const toDateTimeLocal = (value) => {
  if (!value) return ''
  const date = new Date(value)
  const offset = date.getTimezoneOffset()
  const localDate = new Date(date.getTime() - offset * 60000)
  return localDate.toISOString().slice(0, 16)
}

const normalizePayload = (item) => {
  const formatForBackend = (value) => {
    if (!value) return null
    return new Date(value).toISOString()
  }

  return {
    contact: item.contact,
    company: item.company || null,
    deal: item.deal || null,
    interaction_type: item.interaction_type,
    subject: item.subject,
    notes: item.notes || '',
    interaction_date: formatForBackend(item.interaction_date),
    follow_up_date: formatForBackend(item.follow_up_date),
  }
}

const editItem = (item) => {
  editedIndex.value = interactions.value.indexOf(item)
  editedItem.value = {
    ...item,
    interaction_date: toDateTimeLocal(item.interaction_date),
    follow_up_date: toDateTimeLocal(item.follow_up_date),
  }
  dialog.value = true
}

const deleteItem = async (item) => {
  if (confirm('Are you sure you want to delete this interaction?')) {
    try {
      await crmService.deleteInteraction(item.id)
      await loadInteractions()
    } catch (err) {
      console.error('Failed to delete interaction:', err)
      error.value = 'Failed to delete interaction.'
    }
  }
}

const close = () => {
  dialog.value = false
  setTimeout(() => {
    editedItem.value = { ...defaultItem }
    editedIndex.value = -1
    error.value = ''
  }, 300)
}

const save = async () => {
  error.value = ''

  if (!editedItem.value.contact) {
    error.value = 'Please select a contact.'
    return
  }

  if (!editedItem.value.subject?.trim()) {
    error.value = 'Please enter a subject.'
    return
  }

  if (!editedItem.value.interaction_date) {
    error.value = 'Please enter the interaction date.'
    return
  }

  if (
    editedItem.value.follow_up_date &&
    new Date(editedItem.value.follow_up_date) < new Date(editedItem.value.interaction_date)
  ) {
    error.value = 'Follow-up date cannot be earlier than the interaction date.'
    return
  }

  try {
    const payload = normalizePayload(editedItem.value)

    if (editedIndex.value > -1) {
      await crmService.updateInteraction(editedItem.value.id, payload)
    } else {
      await crmService.createInteraction(payload)
    }

    await loadInteractions()
    close()
  } catch (err) {
    console.error('Failed to save interaction:', err)
    error.value =
      err.response?.data?.follow_up_date?.[0] ||
      err.response?.data?.company?.[0] ||
      err.response?.data?.deal?.[0] ||
      err.response?.data?.contact?.[0] ||
      err.response?.data?.subject?.[0] ||
      'Failed to save interaction.'
  }
}

const getInteractionInitials = (subject) => {
  if (!subject) return '?'
  const words = subject.trim().split(' ')
  if (words.length >= 2) return words[0][0] + words[1][0]
  return subject.slice(0, 2).toUpperCase()
}
</script>

<template>
  <v-container fluid class="pa-6">
    <v-row>
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center mb-6 flex-wrap gap-3">
          <div>
            <h1 class="text-h3 font-weight-bold text-navy mb-2">Interactions</h1>
            <p class="text-h6 text-grey-darken-1">
              Track calls, emails, meetings, and notes
              <span class="font-weight-bold">({{ interactions.length }})</span>
            </p>
          </div>
          <v-btn color="primary" size="large" prepend-icon="mdi-plus" @click="dialog = true" elevation="2">
            Add Interaction
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card elevation="2" class="mb-4">
          <v-card-text class="pa-4">
            <div class="d-flex align-center gap-3 flex-wrap mb-4">
              <v-text-field
                v-model="search"
                prepend-inner-icon="mdi-magnify"
                label="Search interactions..."
                variant="outlined"
                density="compact"
                hide-details
                clearable
                class="flex-grow-1"
                style="max-width: 420px;"
              />
              <v-spacer />
              <v-btn-toggle v-model="viewMode" mandatory variant="outlined" divided density="compact">
                <v-btn value="card" size="small"><v-icon>mdi-view-grid</v-icon></v-btn>
                <v-btn value="table" size="small"><v-icon>mdi-view-list</v-icon></v-btn>
              </v-btn-toggle>
            </div>

            <v-row>
              <v-col cols="12" sm="6" md="3">
                <v-select
                  v-model="selectedType"
                  :items="interactionTypeOptions"
                  label="Filter by Type"
                  variant="outlined"
                  density="compact"
                  clearable
                  hide-details
                />
              </v-col>

              <v-col cols="12" sm="6" md="3">
                <v-select
                  v-model="selectedContact"
                  :items="contacts"
                  item-title="email"
                  item-value="id"
                  label="Filter by Contact"
                  variant="outlined"
                  density="compact"
                  clearable
                  hide-details
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item
                      v-bind="props"
                      :title="`${item.raw.first_name} ${item.raw.last_name}`"
                      :subtitle="item.raw.email"
                    />
                  </template>
                  <template v-slot:selection="{ item }">
                    {{ item.raw.first_name }} {{ item.raw.last_name }}
                  </template>
                </v-select>
              </v-col>

              <v-col cols="12" sm="6" md="3">
                <v-select
                  v-model="selectedCompany"
                  :items="companies"
                  item-title="name"
                  item-value="id"
                  label="Filter by Company"
                  variant="outlined"
                  density="compact"
                  clearable
                  hide-details
                />
              </v-col>

              <v-col cols="12" sm="6" md="3">
                <v-select
                  v-model="selectedFollowUpStatus"
                  :items="followUpStatusOptions"
                  label="Follow-up Status"
                  variant="outlined"
                  density="compact"
                  clearable
                  hide-details
                />
              </v-col>
            </v-row>

            <div class="d-flex align-center justify-end mt-4 gap-2 flex-wrap">
              <v-chip
                v-if="activeFiltersCount > 0"
                color="primary"
                variant="tonal"
                size="small"
              >
                {{ activeFiltersCount }} active filter<span v-if="activeFiltersCount > 1">s</span>
              </v-chip>

              <v-btn variant="outlined" color="primary" @click="applyFilters">
                Apply Filters
              </v-btn>

              <v-btn variant="text" color="grey-darken-1" @click="clearFilters">
                Clear Filters
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-if="error && !dialog">
      <v-col cols="12">
        <v-alert type="error" variant="tonal" class="mb-4" closable @click:close="error = ''">
          {{ error }}
        </v-alert>
      </v-col>
    </v-row>

    <v-row v-if="loading">
      <v-col cols="12" class="text-center py-12">
        <v-progress-circular indeterminate color="primary" size="64" />
      </v-col>
    </v-row>

    <v-row v-else-if="viewMode === 'card'">
      <v-col v-for="(interaction, index) in filteredInteractions" :key="interaction.id" cols="12" sm="6" md="4" lg="3">
        <v-card elevation="3" class="interaction-card h-100" hover>
          <v-card-text class="pa-4">
            <div class="d-flex align-center mb-3">
              <v-avatar :color="getInteractionColor(index)" size="48" class="mr-3">
                <span class="text-h6 font-weight-bold text-white">
                  {{ getInteractionInitials(interaction.subject) }}
                </span>
              </v-avatar>
              <div class="flex-grow-1">
                <h3 class="text-h6 font-weight-bold text-truncate mb-1">{{ interaction.subject }}</h3>
                <div class="d-flex align-center gap-2 flex-wrap">
                  <v-chip
                    :color="getTypeColor(interaction.interaction_type)"
                    size="x-small"
                    variant="flat"
                    class="text-capitalize font-weight-bold"
                    :prepend-icon="getTypeIcon(interaction.interaction_type)"
                  >
                    {{ interaction.interaction_type }}
                  </v-chip>

                  <v-chip
                    v-if="interaction.is_follow_up_overdue"
                    color="error"
                    size="x-small"
                    variant="flat"
                    prepend-icon="mdi-alert"
                  >
                    Overdue
                  </v-chip>
                </div>
              </div>
            </div>

            <v-divider class="my-3" />

            <div class="interaction-details">
              <div class="d-flex align-center mb-2" v-if="interaction.contact_name">
                <v-icon size="small" class="mr-2" color="grey-darken-1">mdi-account</v-icon>
                <span class="text-caption font-weight-medium">{{ interaction.contact_name }}</span>
              </div>

              <div class="d-flex align-center mb-2" v-if="interaction.company_name">
                <v-icon size="small" class="mr-2" color="grey-darken-1">mdi-office-building</v-icon>
                <span class="text-caption">{{ interaction.company_name }}</span>
              </div>

              <div class="d-flex align-center mb-2" v-if="interaction.deal_title">
                <v-icon size="small" class="mr-2" color="grey-darken-1">mdi-handshake</v-icon>
                <span class="text-caption">{{ interaction.deal_title }}</span>
              </div>

              <div class="d-flex align-center mb-2">
                <v-icon size="small" class="mr-2" color="grey-darken-1">mdi-calendar-clock</v-icon>
                <span class="text-caption">{{ formatDateTime(interaction.interaction_date) }}</span>
              </div>

              <div class="d-flex align-center" v-if="interaction.follow_up_date">
                <v-icon
                  size="small"
                  class="mr-2"
                  :color="interaction.is_follow_up_overdue ? 'error' : 'grey-darken-1'"
                >
                  mdi-calendar-alert
                </v-icon>
                <span
                  class="text-caption"
                  :class="{ 'text-error font-weight-bold': interaction.is_follow_up_overdue }"
                >
                  {{ formatDateTime(interaction.follow_up_date) }}
                </span>
              </div>
            </div>
          </v-card-text>

          <v-card-actions class="pa-3 pt-0">
            <v-btn size="small" variant="text" color="primary" prepend-icon="mdi-pencil" @click="editItem(interaction)">
              Edit
            </v-btn>
            <v-spacer />
            <v-btn size="small" variant="text" color="error" icon="mdi-delete" @click="deleteItem(interaction)" />
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col v-if="filteredInteractions.length === 0" cols="12">
        <v-card elevation="2" class="pa-12">
          <div class="text-center">
            <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-message-text-outline</v-icon>
            <h3 class="text-h5 mb-2 text-grey-darken-1">No interactions found</h3>
            <p class="text-body-2 text-grey mb-4">
              {{ search || activeFiltersCount ? 'Try adjusting your search or filters' : 'Get started by adding your first interaction' }}
            </p>
            <v-btn v-if="!search && !activeFiltersCount" color="primary" @click="dialog = true" prepend-icon="mdi-plus">
              Add Interaction
            </v-btn>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col cols="12">
        <v-card elevation="3">
          <v-data-table :headers="headers" :items="filteredInteractions" :loading="loading" items-per-page="15">
            <template v-slot:item.subject="{ item, index }">
              <div class="d-flex align-center py-2">
                <v-avatar :color="getInteractionColor(index)" size="36" class="mr-3">
                  <span class="text-caption font-weight-bold text-white">
                    {{ getInteractionInitials(item.subject) }}
                  </span>
                </v-avatar>
                <span class="font-weight-medium">{{ item.subject }}</span>
              </div>
            </template>

            <template v-slot:item.interaction_type="{ item }">
              <v-chip
                :color="getTypeColor(item.interaction_type)"
                size="small"
                variant="flat"
                class="text-capitalize font-weight-bold"
                :prepend-icon="getTypeIcon(item.interaction_type)"
              >
                {{ item.interaction_type }}
              </v-chip>
            </template>

            <template v-slot:item.contact_name="{ item }">
              <span v-if="item.contact_name">{{ item.contact_name }}</span>
              <span v-else class="text-grey">-</span>
            </template>

            <template v-slot:item.company_name="{ item }">
              <span v-if="item.company_name">{{ item.company_name }}</span>
              <span v-else class="text-grey">-</span>
            </template>

            <template v-slot:item.deal_title="{ item }">
              <span v-if="item.deal_title">{{ item.deal_title }}</span>
              <span v-else class="text-grey">-</span>
            </template>

            <template v-slot:item.interaction_date="{ item }">
              {{ formatDateTime(item.interaction_date) }}
            </template>

            <template v-slot:item.follow_up_date="{ item }">
              <div v-if="item.follow_up_date" class="d-flex align-center gap-2 flex-wrap">
                <span :class="{ 'text-error font-weight-bold': item.is_follow_up_overdue }">
                  {{ formatDateTime(item.follow_up_date) }}
                </span>
                <v-chip
                  v-if="item.is_follow_up_overdue"
                  color="error"
                  size="x-small"
                  variant="flat"
                >
                  Overdue
                </v-chip>
              </div>
              <span v-else class="text-grey">-</span>
            </template>

            <template v-slot:item.actions="{ item }">
              <v-icon size="small" class="mr-2" @click="editItem(item)" color="primary">mdi-pencil</v-icon>
              <v-icon size="small" @click="deleteItem(item)" color="error">mdi-delete</v-icon>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="760px" persistent>
      <v-card>
        <v-card-title class="pa-4 bg-grey-lighten-4">
          <div class="d-flex align-center">
            <v-icon class="mr-2" color="primary">
              {{ editedIndex === -1 ? 'mdi-message-plus' : 'mdi-message-edit' }}
            </v-icon>
            <span class="text-h6 font-weight-bold">
              {{ editedIndex === -1 ? 'New Interaction' : 'Edit Interaction' }}
            </span>
          </div>
        </v-card-title>

        <v-divider />

        <v-card-text class="pa-6">
          <v-alert
            v-if="error"
            type="error"
            variant="tonal"
            class="mb-4"
            closable
            @click:close="error = ''"
          >
            {{ error }}
          </v-alert>

          <v-container>
            <v-row>
              <v-col cols="12" sm="6">
                <v-select
                  v-model="editedItem.contact"
                  :items="contacts"
                  item-title="email"
                  item-value="id"
                  label="Contact *"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-account"
                  required
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item
                      v-bind="props"
                      :title="`${item.raw.first_name} ${item.raw.last_name}`"
                      :subtitle="item.raw.email"
                    />
                  </template>
                  <template v-slot:selection="{ item }">
                    {{ item.raw.first_name }} {{ item.raw.last_name }}
                  </template>
                </v-select>
              </v-col>

              <v-col cols="12" sm="6">
                <v-select
                  v-model="editedItem.interaction_type"
                  :items="interactionTypeOptions"
                  label="Interaction Type *"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-shape"
                  required
                />
              </v-col>

              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.subject"
                  label="Subject *"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-text"
                  required
                />
              </v-col>

              <v-col cols="12" sm="6">
                <v-select
                  v-model="editedItem.company"
                  :items="companies"
                  item-title="name"
                  item-value="id"
                  label="Company"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-office-building"
                  clearable
                />
              </v-col>

              <v-col cols="12" sm="6">
                <v-select
                  v-model="editedItem.deal"
                  :items="deals"
                  item-title="title"
                  item-value="id"
                  label="Deal"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-handshake"
                  clearable
                />
              </v-col>

              <v-col cols="12">
                <v-textarea
                  v-model="editedItem.notes"
                  label="Notes"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-note-text"
                  rows="4"
                />
              </v-col>

              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="editedItem.interaction_date"
                  label="Interaction Date *"
                  type="datetime-local"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-calendar-clock"
                  required
                />
              </v-col>

              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="editedItem.follow_up_date"
                  label="Follow-up Date"
                  type="datetime-local"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-calendar-alert"
                />
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>

        <v-divider />

        <v-card-actions class="pa-4">
          <v-spacer />
          <v-btn color="grey" variant="text" @click="close" size="large">Cancel</v-btn>
          <v-btn color="primary" variant="flat" @click="save" size="large" prepend-icon="mdi-content-save">
            Save Interaction
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<style scoped>
.interaction-card {
  transition: all 0.3s ease;
  border-top: 4px solid transparent;
}

.interaction-card:hover {
  transform: translateY(-4px);
  border-top-color: rgb(var(--v-theme-primary));
}

.interaction-details {
  min-height: 120px;
}

.text-navy {
  color: #1a237e;
}
</style>