import { initializeApp } from "firebase/app";
import { getAuth, signOut } from "firebase/auth";
import { getAnalytics } from "firebase/analytics";
import { getStorage, ref, uploadBytesResumable, getDownloadURL } from "firebase/storage";
import {
    getFirestore,
    doc,
    setDoc,
    getDoc,
    getDocs,
    updateDoc,
    arrayUnion,
    arrayRemove,
    collection,
    query,
    where
} from "firebase/firestore";
const firebaseConfig = {
  apiKey: process.env.key,
  authDomain: process.env.domain,
  projectId: process.env.pid,
  storageBucket: process.env.bucket,
  messagingSenderId: "696235957039",
  appId: "1:696235957039:web:fe6eef42b5003b757a5fda",
  measurementId: "G-Q59LQZ3BZQ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const db = getFirestore();
const storage = getStorage();

// doc(db, collection, document-id, { document data })
export const addNFTToDB = async (file) => {
    const file_id = new Date().getTime().toString()
    // Adding file to our storage.

    // Creating the file metadata
    const metadata = { contentType: file.type };

    // Uploading file and metadata
    const storageRef = ref(storage, 'files/' + file_id);
    const uploadTask = uploadBytesResumable(storageRef, file, metadata);

    // Listen for state changes, errors, and completion of the upload.
    return new Promise((resolve, reject) => {
        uploadTask.on('state_changed',
            (snapshot) => {
                // Get task progress, including the number of bytes uploaded and the total number of bytes to be uploaded
                const progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
                console.log('Upload is ' + progress + '% done');
                switch (snapshot.state) {
                  case 'paused':
                    console.log('Upload is paused');
                    break;
                  case 'running':
                    console.log('Upload is running');
                    break;
                }
            },
        (error) => {
            switch (error.code) {
              case 'storage/unauthorized':
                // User doesn't have permission to access the object
                break;
              case 'storage/canceled':
                // User canceled the upload
                break;
              case 'storage/unknown':
                // Unknown error occurred, inspect error.serverResponse
                break;
            default:
                reject()
                break;
            }
        },
        () => {
            // Upload completed successfully, now we can get the download URL
            getDownloadURL(uploadTask.snapshot.ref).then(async (downloadURL) => {
                // console.log('File available at', downloadURL);

                // return 'success'
                resolve(downloadURL)
            })
        })
    })
}
