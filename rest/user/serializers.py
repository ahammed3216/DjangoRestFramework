from django.contrib.auth.models import User
from rest_framework import serializers,validators


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username','password','first_name','last_name','email')

        extra_kwags={
            "password":{"write_only":True},
            "email":{
                    "required":True,
                    "allow_blank":False,
                    "validators":[
                        validators.UniqueValidator(User.objects.all(),"User with same email id exist")
                    ]
            }
        }

        def create(self,request):
            username=validated_data.get('username')
            first_name=validated_data.get('first_name')
            last_name=validated_data.get('last_name')
            password=validated_data.get('password')
            email=validated_data.get('email')
            user=User.object.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                email=email
            )

            return user