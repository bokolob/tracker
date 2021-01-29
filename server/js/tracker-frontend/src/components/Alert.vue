<template>
<div class="modal fade" :id="id" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="staticBackdropLabel">{{title}}</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        {{body}}
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary" @click="accepted">Understood</button>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import { Modal } from 'bootstrap'

export default {
    props: ['show', 'body', 'title'],
    data() {
        return {id: null, modal: null}
    },
    created() {
        this.id = this._uid
    },
    mounted() {
        let element = document.getElementById(this.id);
        this.modal = new Modal(element, {keyboard: false});

        element.addEventListener('hidden.bs.modal', () => {
           this.$emit('closed'); 
        });
    },
    methods: {
        accepted() {
            this.$emit('accepted');
        }
    },
    watch: {
        'show' : {
            handler(newValue) {
                if (newValue) {
                    this.modal.show(); 
                }
                else {
                   this.modal.hide();  
                }
            }
        }
    }    
}
</script>
