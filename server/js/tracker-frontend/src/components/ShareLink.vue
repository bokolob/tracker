<template>
    <button class="btn btn-link btn-sm btn-warning" :data-clipboard-text="data_for_sharing" @click="sendlink" id="sharing_link">Share!</button>
</template>

<script>
    export default {
        props: ['data_for_sharing'],
        methods: {
            sendlink() {
            navigator.share({
                title: 'WebShare API Demo',
                text: 'Check out web.dev.',
                url: this.data_for_sharing,
                },
                {
                    copy: true,
                    email: true,
                    messenger: true,
                    facebook: true,
                    whatsapp: true,
                    telegram: true,
                    skype: true,
                    language: 'ru' // specify the default language
                }
                ).then(() => {
                    console.log('Thanks for sharing!');
                })
                .catch( (e) => alert(e));
                return false;
            }, 
        },
    }
</script>